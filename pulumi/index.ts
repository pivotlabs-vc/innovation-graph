
import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";
import { local } from "@pulumi/command";

const webVersion = process.env.WEB_IMAGE_VERSION;
const sparqlVersion = process.env.SPARQL_IMAGE_VERSION;

if (!webVersion)
    throw Error("WEB_IMAGE_VERSION not defined");

if (!sparqlVersion)
    throw Error("SPARQL_IMAGE_VERSION not defined");

if (!process.env.ARTIFACT_REPO)
    throw Error("ARTIFACT_REPO not defined");

if (!process.env.ARTIFACT_REPO_REGION)
    throw Error("ARTIFACT_REPO_REGION not defined");

if (!process.env.ARTIFACT_NAME)
    throw Error("ARTIFACT_NAME not defined");

if (!process.env.WEB_HOSTNAME)
    throw Error("WEB_HOSTNAME not defined");

if (!process.env.GCP_PROJECT)
    throw Error("GCP_PROJECT not defined");

if (!process.env.GCP_REGION)
    throw Error("GCP_REGION not defined");

if (!process.env.ENVIRONMENT)
    throw Error("ENVIRONMENT not defined");

if (!process.env.CLOUD_RUN_REGION)
    throw Error("CLOUD_RUN_REGION not defined");

if (!process.env.DNS_DOMAIN_DESCRIPTION)
    throw Error("DNS_DOMAIN_DESCRIPTION not defined");

if (!process.env.DOMAIN)
    throw Error("DOMAIN not defined");

if (!process.env.WEB_MIN_SCALE)
    throw Error("WEB_MIN_SCALE not defined");

if (!process.env.WEB_MAX_SCALE)
    throw Error("WEB_MAX_SCALE not defined");

if (!process.env.SPARQL_MIN_SCALE)
    throw Error("SPARQL_MIN_SCALE not defined");

if (!process.env.SPARQL_MAX_SCALE)
    throw Error("SPARQL_MAX_SCALE not defined");

const provider = new gcp.Provider(
    "gcp",
    {
	project: process.env.GCP_PROJECT,
	region: process.env.GCP_REGION,
    }
);

const enableCloudRun = new gcp.projects.Service(
    "enable-cloud-run",
    {
	service: "run.googleapis.com",
    },
    {
	provider: provider
    }
);

const enableComputeEngine = new gcp.projects.Service(
    "enable-compute-engine",
    {
	service: "compute.googleapis.com",
    },
    {
	provider: provider
    }
);

const enableCloudDns = new gcp.projects.Service(
    "enable-cloud-dns",
    {
	service: "dns.googleapis.com",
    },
    {
	provider: provider
    }
);

const enableArtifactRegistry = new gcp.projects.Service(
    "enable-artifact-registry",
    {
	service: "artifactregistry.googleapis.com",
    },
    {
	provider: provider
    }
);

const repo = process.env.ARTIFACT_REPO;

const artifactRepo = new gcp.artifactregistry.Repository(
    "artifact-repo",
    {
	description: "repository for " + process.env.ENVIRONMENT,
	format: "DOCKER",
	location: process.env.ARTIFACT_REPO_REGION,
	repositoryId: process.env.ARTIFACT_NAME,
    },
    {
	provider: provider,
	dependsOn: enableArtifactRegistry,
    }
);

const localWebImageName = "web:" + webVersion;
const localSparqlImageName = "sparql:" + sparqlVersion;

const webImageName = repo + "/web:" + webVersion;
const sparqlImageName = repo + "/sparql:" + sparqlVersion;

const taggedWebImage = new local.Command(
    "web-docker-tag-command",
    {
	create: "docker tag " + localWebImageName + " " + webImageName,
    }
);

const taggedSparqlImage = new local.Command(
    "sparql-docker-tag-command",
    {
	create: "docker tag " + localSparqlImageName + " " + sparqlImageName,
    }
);

const webImage = new local.Command(
    "web-docker-push-command",
    {
	create: "docker push " + webImageName,
    },
    {
	dependsOn: [taggedWebImage, artifactRepo],
    }
);

const sparqlImage = new local.Command(
    "sparql-docker-push-command",
    {
	create: "docker push " + sparqlImageName,
    },
    {
	dependsOn: [taggedSparqlImage, artifactRepo],
    }
);

const sparqlService = new gcp.cloudrun.Service(
    "sparql-service",
    {
	name: "sparql-" + process.env.ENVIRONMENT,
	location: process.env.CLOUD_RUN_REGION,
	template: {
	    metadata: {
		labels: {
		    version: "v" + sparqlVersion.replace(/\./g, "-"),
		},		
		annotations: {
                    "autoscaling.knative.dev/minScale": process.env.SPARQL_MIN_SCALE,
                    "autoscaling.knative.dev/maxScale": process.env.SPARQL_MAX_SCALE,
		}
	    },
            spec: {
		containerConcurrency: 1000,
		containers: [
		    {
			image: sparqlImageName,
			ports: [
                            {
				"name": "http1", // Must be http1 or h2c.
				"containerPort": 8089
                            }
			],
			resources: {
                            limits: {
				cpu: "1000m",
				memory: "256Mi",
                            }
			},
		    }
		],
            },
	},
    },
    {
	provider: provider,
	dependsOn: [enableCloudRun, sparqlImage],
    }
);

const sparqlUrl = sparqlService.statuses[0].url;

export const sparqlResource = sparqlUrl.apply(
    x => x.replace(/^https:\/\//, "")
);

const webService = new gcp.cloudrun.Service(
    "web-service",
    {
	name: "web-" + process.env.ENVIRONMENT,
	location: process.env.CLOUD_RUN_REGION,
	template: {
	    metadata: {
		labels: {
		    version: "v" + webVersion.replace(/\./g, "-"),
		},		
		annotations: {
                    "autoscaling.knative.dev/minScale": process.env.WEB_MIN_SCALE,
                    "autoscaling.knative.dev/maxScale": process.env.WEB_MAX_SCALE,
		}
	    },
            spec: {
		containerConcurrency: 1000,
		containers: [
		    {
			image: webImageName,
			ports: [
                            {
				"name": "http1", // Must be http1 or h2c.
				"containerPort": 8080
                            }
			],
			commands: [
			    "/usr/local/bin/serve",
			    "0:8080",                // Listen
			    sparqlResource,	     // SPARQL API resource
			    "https",		     // SPARQL scheme
			    ".",		     // Base
			],
			envs: [
                            { name: "ASD", value: "DEF" }
			],
			resources: {
                            limits: {
				cpu: "1000m",
				memory: "256Mi",
                            }
			},
		    }
		],
            },
	},
    },
    {
	provider: provider,
	dependsOn: [enableCloudRun, webImage],
    }
);

const allUsersPolicy = gcp.organizations.getIAMPolicy(
    {
	bindings: [{
            role: "roles/run.invoker",
            members: ["allUsers"],
	}],
    },
    {
	provider: provider,
    }
);

const webNoAuthPolicy = new gcp.cloudrun.IamPolicy(
    "web-no-auth-policy",
    {
	location: webService.location,
	project: webService.project,
	service: webService.name,
	policyData: allUsersPolicy.then(pol => pol.policyData),
    },
    {
	provider: provider,
    }
);

const sparqlNoAuthPolicy = new gcp.cloudrun.IamPolicy(
    "sparql-no-auth-policy",
    {
	location: sparqlService.location,
	project: sparqlService.project,
	service: sparqlService.name,
	policyData: allUsersPolicy.then(pol => pol.policyData),
    },
    {
	provider: provider,
    }
);

const webDomainMapping = new gcp.cloudrun.DomainMapping(
    "web-domain-mapping",
    {
	"name": process.env.WEB_HOSTNAME,
	location: process.env.CLOUD_RUN_REGION,
	metadata: {
	    namespace: "pivot-labs",
	},
	spec: {
	    routeName: webService.name,
	}
    },
    {
	provider: provider
    }
);

// Get rrdata from domain mapping.
export const webhost = webDomainMapping.statuses.apply(
    x => x[0].resourceRecords
).apply(
    x => x ? x[0] : { rrdata: "" }
).apply(
    x => x.rrdata
);

const zone = new gcp.dns.ManagedZone(
    "zone",
    {
	name: process.env.DNS_DOMAIN_DESCRIPTION,
	description: process.env.DOMAIN,
	dnsName: process.env.DOMAIN,
	labels: {
	},
    },
    {
	provider: provider,
	dependsOn: [enableCloudDns],
    }
);

const recordSet = new gcp.dns.RecordSet(
    "web-record",
    {
	name: process.env.WEB_HOSTNAME + ".",
	managedZone: zone.name,
	type: "CNAME",
	ttl: 300,
	rrdatas: [webhost],
    },
    {
	provider: provider,
	dependsOn: zone,
    }
);

const sparqlServiceMon = new gcp.monitoring.GenericService(
    "sparql-service-monitoring",
    {
	basicService: {
            serviceLabels: {
		service_name: sparqlService.name,
		location: process.env.CLOUD_RUN_REGION,
            },
            serviceType: "CLOUD_RUN",
	},
	displayName: "SPARQL service (" + process.env.ENVIRONMENT + ")",
	serviceId: "sparql-service-" + process.env.ENVIRONMENT + "-mon",
	userLabels: {
	    "service": sparqlService.name,
	    "application": "sparql-service",
	    "environment": process.env.ENVIRONMENT,
	},
    },
    {
	provider: provider,
    }
);

const webServiceMon = new gcp.monitoring.GenericService(
    "web-service-monitoring",
    {
	basicService: {
            serviceLabels: {
		service_name: webService.name,
		location: process.env.CLOUD_RUN_REGION,
            },
            serviceType: "CLOUD_RUN",
	},
	displayName: "Web service (" + process.env.ENVIRONMENT + ")",
	serviceId: "web-service-" + process.env.ENVIRONMENT + "-mon",
	userLabels: {
	    "service": webService.name,
	    "application": "web-service",
	    "environment": process.env.ENVIRONMENT,
	},
    },
    {
	provider: provider,
    }
);

const sparlLatencySlo = new gcp.monitoring.Slo(
    "requestBasedSlo",
    {
	service: sparqlServiceMon.serviceId,
	sloId: "sparql-service-" + process.env.ENVIRONMENT + "-latency-slo",
	displayName: "SPARQL latency (" + process.env.ENVIRONMENT + ")",
	goal: 0.9,
	rollingPeriodDays: 5,
	windowsBasedSli: {
	    windowPeriod: "300s",
	    goodTotalRatioThreshold: {
		basicSliPerformance: {
		    latency: {
			threshold: "0.1s"
		    }
		},
		threshold: 0.9,
	    }
	}
    },
    {
	provider: provider,
    }
);
	
