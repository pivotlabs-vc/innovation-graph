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

const webVersion = "0.4.0";
const webImage = "europe-west1-docker.pkg.dev/pivot-labs/pivot-labs/web:" +
      webVersion;

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

export const url = webService.statuses[0].url;
