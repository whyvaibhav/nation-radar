import re

class RegexFilter:
    def __init__(self, project_keywords=None, false_positives=None):
        self.project_keywords = project_keywords or []
        self.false_positives = false_positives or []

    def is_relevant(self, text):
        t = text.lower()
        fp_matches = [p for p in self.false_positives if re.search(p, t)]
        if fp_matches:
            project_matches = [p for p in self.project_keywords if re.search(p, t)]
            return bool(project_matches)
        project_matches = [p for p in self.project_keywords if re.search(p, t)]
        return bool(project_matches) 