from datetime import datetime, date


def format_month_year(value) -> str:
    if not value:
        return "No Date"

    if isinstance(value, (datetime, date)):
        return value.strftime("%b %-d, %Y")

    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%b %-d, %Y")
        except ValueError:
            return value

    return "No Date"


def get_issue_title(issue) -> str:
    """Returns a formatted title: 'Series Name #1' or just 'Issue #1'"""
    if issue.series and issue.series.name:
        return f"{issue.series.name} #{issue.number}"
    return f"Issue #{issue.number}"
