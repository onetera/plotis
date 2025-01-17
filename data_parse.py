import re

def parse_budget(data):
    result = {
        "headers": ["항목", "기간", "세부항목", "가격"],
        "tasks": [],
        "footer": {
            "totalLabel": "Total",
            "totalPrice": 0
        }
    }
    current_section = None

    for line in data.splitlines():
        section_match = re.match(r"\| ([^|]+)\s+\|", line)
        if section_match and not re.search(r"\d주", line):
            current_section = section_match.group(1).strip()

        task_match = re.match(r"\|\s+\|\s+(\d+주)\s+\|\s+([^|]+)\s+\|\s+([\d,]+)\s+\|", line)
        if task_match and current_section:
            duration, name, value = task_match.groups()
            value_cleaned = int(value.replace(",", ""))
            result["tasks"].append({
                "title": current_section,
                "duration": duration.strip(),
                "name": name.strip(),
                "value": value_cleaned
            })
    
    return result


def parse_schedule(data):
    result = {"schedules": []}
    colors = ["#ff3b2f", "#ff9500", "#35c759", "#00c7be"]

    for line in data.splitlines():
        section_match = re.match(r"## \d+\. (.+)", line)
        if section_match:
            if 'current_section' in locals():
                current_section["totalWeeks"] = sum(task["duration"] for task in current_section["tasks"])
                result["schedules"].append(current_section)
            
            current_section = {
                "title": section_match.group(1),
                "colors": colors,
                "tasks": []
            }
            color_index = len(result["schedules"]) % len(colors)

        task_match = re.match(r"#### (.+)", line)
        if task_match and 'current_section' in locals():
            task_name = task_match.group(1).strip()

        duration_match = re.match(r"- 기간: (\d+)주", line)
        if duration_match and 'current_section' in locals() and task_name:
            duration = int(duration_match.group(1))
            current_section["tasks"].append({
                "name": task_name,
                "duration": duration,
                "colorIndex": color_index
            })

    if 'current_section' in locals():
        current_section["totalWeeks"] = sum(task["duration"] for task in current_section["tasks"])
        result["schedules"].append(current_section)

    return result