# autoDep
The auto deployment pipeline is a comprehensive process that automates the deployment of updates to various sites within the infrastructure. The process starts by accessing the Jenkins Web Interface via the Virtual Private Network (VPN). From there, users can initiate the auto deployment pipeline, which triggers a cascade of events.

The first step involves pulling a cluster that contains a list of sites and their corresponding details, such as server host names and IP addresses. For each site, a parallel process is initiated, which consists of sending update commands and monitoring the progress of the updates. These updates are pulled from the Gitea Repository Server, ensuring that the latest versions of applications are deployed.

Once a single site completes the update process, an endpoint on the Toolbox Server, which acts as a monolith server, is invoked. This endpoint triggers the sending of an alert to the appropriate respondent(s) via email or SMS. This ensures that the relevant individuals are promptly notified about the completion of the update process for a specific site.

Throughout the entire auto deployment pipeline process, the Jenkins Web Interface provides real-time printouts and status updates, acting as a monitoring tool. It allows users to track the progress of each step, identify any issues or errors, and take necessary actions to ensure a smooth and successful deployment.
