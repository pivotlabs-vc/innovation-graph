import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

// Create a GCP resource (Storage Bucket)
//const bucket = new gcp.storage.Bucket("my-bucket", {
//    location: "US"
//});

// Export the DNS name of the bucket
//export const bucketName = bucket.url;

/*
const project = new gcp.projects.Service("project", {
    disableDependentServices: true,
    project: "your-project-id",
    service: "iam.googleapis.com",
}, { timeouts: {
    create: "30m",
    update: "40m",
} });
*/

const provider = new gcp.Provider(
    "gcp",
    {
	project: "pivot-labs",
	region: "eu-west1",
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

const repo = "europe-west1-docker.pkg.dev/pivot-labs/pivot-labs";

const webVersion = "0.4.0";
const webImage = repo + "/web:" + webVersion;

const sparqlVersion = "0.4.0";
const sparqlImage = repo + "/sparql:" + sparqlVersion;

const sparqlService = new gcp.cloudrun.Service(
    "sparql-service",
    {
	name: "sparql",
	location: "europe-west1",
	template: {
	    metadata: {
		labels: {
		    version: "v" + sparqlVersion.replace(/\./g, "-"),
		},		
		annotations: {
                    "autoscaling.knative.dev/minScale": "0",
                    "autoscaling.knative.dev/maxScale": "1",
		}
	    },
            spec: {
		containerConcurrency: 1000,
		containers: [
		    {
			image: sparqlImage,
			ports: [
                            {
				"name": "http1", // Must be http1 or h2c.
				"containerPort": 8089
                            }
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
	dependsOn: [enableCloudRun],
    }
);

const sparqlUrl = sparqlService.statuses[0].url;

export const sparqlResource = sparqlUrl.apply(
    x => x.replace(/^https:\/\//, "")
);

const webService = new gcp.cloudrun.Service(
    "web-service",
    {
	name: "web",
	location: "europe-west1",
	template: {
	    metadata: {
		labels: {
		    version: "v" + webVersion.replace(/\./g, "-"),
		},		
		annotations: {
                    "autoscaling.knative.dev/minScale": "0",
                    "autoscaling.knative.dev/maxScale": "1",
		}
	    },
            spec: {
		containerConcurrency: 1000,
		containers: [
		    {
			image: webImage,
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
			    "",			     // Base
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
	dependsOn: [enableCloudRun],
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



