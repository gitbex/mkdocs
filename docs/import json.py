import json
import urllib3
import os
import re

http = urllib3.PoolManager()
slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
slack_mentions = os.environ.get("SLACK_MENTIONS", "").split(",")

def format_alarm_reason(message, new_state, trigger):
    """Create a user-friendly reason message"""
    metric_name = trigger.get('MetricName', 'N/A')
    threshold = trigger.get('Threshold')
    statistic = trigger.get('Statistic', 'Average')
    comparison = trigger.get('ComparisonOperator', '')
    evaluation_periods = trigger.get('EvaluationPeriods', 1)
    period = trigger.get('Period', 300)
    
    # Extract actual value from NewStateReason
    reason = message.get('NewStateReason', '')
    value_match = re.search(r'\[([0-9.]+)', reason)
    actual_value = float(value_match.group(1)) if value_match else None
    
    # Format comparison operator
    comparison_text = {
        'GreaterThanOrEqualToThreshold': '≥',
        'GreaterThanThreshold': '>',
        'LessThanOrEqualToThreshold': '≤',
        'LessThanThreshold': '<',
    }.get(comparison, comparison)
    
    # Create user-friendly message
    if new_state == "ALARM":
        if actual_value and threshold:
            return (f":rotating_light: *{metric_name}* is *{actual_value:.2f}%* ({statistic}), "
                   f"which is {comparison_text} threshold of *{threshold}%*")  # FIXED
        else:
            return f":rotating_light: *{metric_name}* exceeded threshold of *{threshold}%*"
    
    elif new_state == "OK":
        if actual_value and threshold:
            return (f":white_check_mark: *{metric_name}* is *{actual_value:.2f}%* ({statistic}), "
                   f"back to normal (threshold: {threshold}%)")
        else:
            return f":white_check_mark: *{metric_name}* returned to normal (threshold: {threshold}%)"  # FIXED
    
    else:
        # Insufficient data or other states
        return f":grey_question: *{metric_name}* state changed to {new_state}"

def lambda_handler(event, context):
    # SNS eventdan message olish
    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(f"Message: {message}")

    # Asosiy fieldlar
    alarm_name = message.get('AlarmName', 'N/A')
    alarm_description = message.get('AlarmDescription', '')
    new_state = message.get('NewStateValue', 'N/A')
    old_state = message.get('OldStateValue', 'N/A')
    reason = message.get('NewStateReason', 'N/A')
    region = message.get('Region', 'N/A')
    trigger = message.get('Trigger', {})
    metric_name = trigger.get('MetricName', 'N/A')
    # namespace = trigger.get('Namespace', 'N/A')
    dimensions = trigger.get('Dimensions', [])
    metrics = trigger.get('Metrics', [])
    attrs = message.get("AlarmContributorAttributes", {})

    # ---- Servis nomini aniqlash ----
    if metrics:
        metric_info = metrics[0]
        service_name = (
            metric_info.get("Label")
            or metric_info.get("Id")
            or alarm_name
        )
    elif "TargetGroup" in attrs:
        service_name = attrs["TargetGroup"].split("/")[1]
    # elif namespace not in (None, "N/A"):
    #     service_name = namespace.replace("AWS/", "Amazon ")
    else:
        service_name = alarm_name

    # ---- Resource nomini olish ----
    if dimensions and isinstance(dimensions, list):
        resource_pairs = [f"{d.get('name')}={d.get('value')}" for d in dimensions if 'name' in d and 'value' in d]
        resource = ', '.join(resource_pairs)
    elif "TargetGroup" in attrs:
        resource = attrs["TargetGroup"]
    else:
        resource = 'N/A'

    if "=" in resource and "," not in resource:
        resource_display = resource.split("=")[-1]
    else:
        resource_display = resource

    # ---- Status formatlash ----
    if new_state == "ALARM":
        status_emoji = ":rotating_light:"
        status_text = "ALERT"
        color = "#FF4C4C"
    elif new_state == "OK":
        status_emoji = ":white_check_mark:"
        status_text = "RESOLVED"
        color = "#36A64F"
    else:
        status_emoji = ":grey_question:"
        status_text = new_state
        color = "#AAAAAA"

    # ---- Mentionlar ----
    mention_text = " ".join([f"<@{m.strip()}>" for m in slack_mentions if m.strip()])

    # ---- Format better reason ----
    formatted_reason = format_alarm_reason(message, new_state, trigger)

    # ---- Slack xabari ----
    fields = [
        {"title": "Alarm Name", "value": alarm_name, "short": False},
        {"title": "Region", "value": region, "short": True},
        {"title": "Metric", "value": metric_name, "short": True},
        {"title": "Resource", "value": f":fire: *{resource_display}*", "short": False},
        {"title": "State Change", "value": f"{old_state} → {new_state}", "short": True},
        {"title": "Summary", "value": formatted_reason, "short": False},
    ]
    
    # Add description if it exists
    if alarm_description:
        fields.insert(1, {"title": "Description", "value": alarm_description, "short": False})

    slack_message = {
        "attachments": [
            {
                "color": color,
                "fallback": f"{service_name} {status_text}: {alarm_name}",
                "text": f"{status_emoji} *{service_name}* {status_text} {mention_text}",
                "fields": fields
            }
        ]
    }

    # ---- Slack'ga yuborish ----
    encoded_data = json.dumps(slack_message).encode("utf-8")
    resp = http.request(
        "POST",
        slack_webhook_url,
        body=encoded_data,
        headers={'Content-Type': 'application/json'}
    )

    print(f"Slack response: {resp.status}")
    return {"statusCode": resp.status, "body": json.dumps({"message": "Alert sent to Slack"})}