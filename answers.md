## Question 4: Detecting Slow APIs (Latency > 2000ms)

To detect API requests that take longer than 2000ms with the dashboard, I would use the Response Times chart which is showing API requests made on the app with consideration on completion times of the requests.
When the average, P90, or P99 response times cross the 2000ms threshold, it signals that the endpoint is slow.

Additionally, I would add a visual threshold line at 2000ms on the chart, which would be helpful to visually monitor and detect API requests that cross the threshold. 

In addition, I would configure alerts based on this metric, for example, if the P90 response time exceeds 2000ms over a certain period, an alert can be triggered.


## Question 5: Detecting High Error Rates (>30%)

To detect when an API has an error rate exceeding 30% I would use the Error Rate element on the dashboard, which shows percentage of errors out of total requests. 

I would add a visual threshold line to easily detect when an API error rate is above 30%. 

I would exclude the "Insufficient funds" error with a different error code and don't include it the error rate monitoring, because its part of business logic and not a failed API.

In addition, I would configure alerts based on this metric, for example, if the error rate remains above 30% for a defined period (for example more than 5 minutes), an alert can be triggered.



## Question 6: Define 5 Alerts for Service Monitoring

#### 5 theoretical alerts to monitor service health: 
1. Slow APIs Alert - an alert that detects slow response times, as described on question 4.
2. High Error Rate Alert - an alert that detects high error rate (calculated as the percentage of requests returning 4xx or 5xx statuses), as described on question 5.
3. Low Request Throughput Alert - an alert that detects when number of requests per second drops significantly. 
4. Service Down Alert - an alert that detects when there are no metrics, this can be done by checking if a key metric like the request counter remains at zero for a sustained period.
5. High Latency Variability Alert - an alert that is triggered when there is a spike at P99 latency metric, even though the average response time is acceptable. This can indicate that specific requests have a high latency.

### A runbook to NOC - to investigate and troubleshoot the issue:

#### Runbook: Investigating High Error Rate Alert
Alert Trigger:
High Error Rate Alert is triggered when the API error rate (HTTP 4xx/5xx responses) exceeds 30% over a 5-minute window.

1. Acknowledge the Alert:
   - Step 1: Acknowledge the alert in the incident management system.
   - Step 2: Document the alert time, affected services, and initial metric values (error rate, total requests, etc.).


2. Verify the Alert in the Dashboard
   - Action: Open the monitoring dashboard (e.g., Grafana) and verify the error rate metric.
   - Key Metrics to Check:
     - Error Rate Panel: Confirm the percentage error.
     - Total Request Throughput: Verify that overall request volumes are as expected.
   - Action: Identify which endpoints are contributing most to the error rate by filtering or grouping by endpoint or HTTP status.


3. Communication:
   - Notify your team-lead or the on-call SRE and the relevant development/infrastructure team of your findings and the planned remediation steps.
   - If necessary notify the affected customer.
   

3. Check Service Health and Logs
   - Step 1: Access the logs for the affected service(s) via your centralized logging tool or directly from container logs.
   Look for patterns such as repeated error messages, exceptions, or stack traces that coincide with the alert time.
   - Step 2: Determine if errors are concentrated on a specific API call (e.g., "withdraw" vs. "deposit").
   - Step 3: Verify service health by checking endpoints such as `/metrics` or `/health` to confirm if the service is partially or fully degraded.


4. Investigate Potential Root Causes
   - Configuration Issues:
     - Review recent configuration changes in the service or upstream dependencies.
     - Confirm that any rate limiting or authentication modifications haven’t inadvertently caused unexpected 4xx errors.
   - Dependency Failures:
     - Check that external dependencies (databases, third-party APIs) are available and responding as expected.
   - Code or Deployment Issues:
     - Identify if a recent deployment introduced bugs that may have increased error responses.
   - Load or Traffic Spikes:
     - Determine whether increased traffic or resource exhaustion (CPU, memory) correlates with the spike in error rate.


5. Take Remedial Actions
   - Short-Term Mitigation:
     - If resource exhaustion is detected, consider scaling the service or restarting the affected container.
     - If a configuration error is identified, roll back to the last known good configuration.


6. Validate the Fix
   - Step 1: After implementing corrective actions, monitor the dashboard to ensure the error rate drops below the threshold.
   - Step 2: Verify that logs indicate normal behavior and that no new errors have been introduced.
   - Step 3: Document the resolution in the incident management system.


7. Postmortem and Preventative Measures
   - Review: Conduct a postmortem analysis to determine the root cause of the error rate spike and document your findings.
   - Preventative Actions: Identify improvements (e.g., enhanced error handling, scaling policies, or improved monitoring) to prevent recurrence.
   - Communication: Share a summary of the incident and the corrective actions taken with the broader team.