# AWS CloudWatch Agent Configuration

## Disk and Memory Metrics

This document outlines the steps to configure the CloudWatch Agent to collect essential Disk and Memory utilization metrics from EC2 instances, ensuring we only collect the necessary data.


#### 1. The Minimized Configuration File  
The configuration below is saved as cloudwatch-agent.json in the `/opt/aws/amazon-cloudwatch-agent/etc/` directory.  
It is scoped only to collect memory and disk metrics.  

If you create or edit the agent configuration file manually, you can give it any name. For simplicity in troubleshooting, we recommend that you name it /opt/aws/  amazon-cloudwatch-agent/etc/cloudwatch-agent.json on a Linux server and $Env:ProgramData\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent.json on servers running Windows Server.   After you have created the file, you can copy it to other servers where you want to install the agent.  

Create and add permissoins  

```BASH
sudo nano cloudwatch-agent.json
sudo chown cwagent:cwagent cloudwatch-agent.json
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-agent.json
```


Add template to config file  

```JSON
{
  "agent": {
    "metrics_collection_interval": 60,
    "region": "us-east-2",
    "logfile": "/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log",
    "debug": false,
    "run_as_user": "cwagent"
  },
  "metrics": {
    "namespace": "CWAgent",
    "metrics_collected": {
      "disk": {
        "measurement": [
          "disk_used_percent",
          "disk_free"
        ],
        "metrics_collection_interval": 60,
        "resources": [
          "*"
        ],
        "ignore_file_system_types": [
          "sysfs",
          "devtmpfs",
          "overlay"
        ]
      },
      "mem": {
        "measurement": [
          "mem_used_percent"
        ],
        "metrics_collection_interval": 60
      }
    },
    "append_dimensions": {
      "ImageId": "${aws:ImageId}",
      "InstanceId": "${aws:InstanceId}",
      "InstanceType": "${aws:InstanceType}",
      "AutoScalingGroupName": "${aws:AutoScalingGroupName}"
    }
  }
}
```

---

#### 2. Apply and Start the Agent Configuration

The configuration is applied using the `amazon-cloudwatch-agent-ctl` utility.

=== "Linux"
    ``` BASH 
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-agent.json
    ```

=== "Windows"

    ``` Powershell
    & "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:"C:\path\to\cloudwatch-agent.json"
    ```

---

#### 3. Verify Agent Status
After running the command above, confirm the agent is running and configured correctly.

Check Status
```BASH
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
```  

Expected Output:

```JSON
{
  "status": "running",
  "configstatus": "configured",
  "version": "..."
}
```

Check Agent Logs for Errors
Check the agent log file (after at least one minute to ensure a collection cycle has occurred) to look for any new errors:

```BASH
tail -n 20 /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log | grep -i 'error'
```

- Expected Behavior: 
No output, or only informational messages

---

[Link for official documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file.html)