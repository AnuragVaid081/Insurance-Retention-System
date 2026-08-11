import json

class InvestigationMemory:

    def __init__(self):
        self.tool_cache = {}
        self.facts = []
        self.evidence = {}
        self.hypotheses = []
        self.lost_business = {
            "categories": {},
            "examples": {}
        }
        self.completed_sections = set()

    def add_tool_result(self,cache_key, tool_name, facts):
        self.tool_cache[cache_key] = {
            "tool": tool_name,
            "facts": facts,
            "lost_business": self.lost_business
        }

    def get_tool_result(self, cache_key):
        return self.tool_cache.get(cache_key)

    def has_tool_result(self, cache_key):
        return cache_key in self.tool_cache

    def has_fact(self, title):

        return any(
        fact["title"] == title
        for fact in self.facts
    )

        # --------------------------------------------------
        # Facts
        # --------------------------------------------------

    def add_fact(self, fact):

        if fact not in self.facts:
            self.facts.append(fact)

    def remove_fact(self, fact):

        if fact in self.facts:
            self.facts.remove(fact)

        self.evidence.pop(fact,None)

        # --------------------------------------------------
        # Hypothesis
        # --------------------------------------------------            

    def add_hypotheses(self, hypothesis):

        if hypothesis not in self.hypotheses:
            self.hypotheses.append(hypothesis)

    def resolve_hypothesis(self, hypothesis):

        if hypothesis in self.hypotheses:
            self.hypotheses.remove(hypothesis)

        # --------------------------------------------------
        # Completed Sections
        # --------------------------------------------------

    def mark_completed(self, section):
        self.completed_sections.add(section)

    def is_completed(self, section):
        return section in self.completed_sections

        # --------------------------------------------------
        # Build Context
        # --------------------------------------------------

    def build_context(self):

        context = []

        context.append("CURRENT INVESTIGATION\n")


        # Facts 
        context.append("Buisness Facts:")

        if self.facts:

            for fact in self.facts:

                context.append(f"\n{fact['title']}")
                context.append(f"- {fact['fact']}")

                context.append("Supporting Statistics:")

                for key, value in fact["statistics"].items():

                    if isinstance(value,dict):

                        context.append(
                            f"    • {key}: "
                            f"{value['count']} "
                            f"({value['percentage']}%)"
                        )

                    elif isinstance(value, list):
                        context.append(f"    • {key}: {len(value)} IMDs")

                        for imd in value[:5]:
                            context.append(
                                f"        - IMD {imd['IMD']} | "
                                f"{imd['Renewal Rate']}% | "
                                f"Portfolio {imd['Portfolio']}"
                            )
                    else:
                        context.append(f"    • {key}: {value}")

        else:
            context.append("- None")

        context.append("")

        # Lost Business Patterns

        if self.lost_business["categories"]:

            context.append("\nLost Business Patterns")

            for category, stats in self.lost_business["categories"].items():

                context.append(
                    f"    • {category}: "
                    f"{stats['count']} "
                    f"({stats['percentage']}%)"
                )

            context.append("\nRepresentative Examples:")

            for category, remarks in self.lost_business["examples"].items():

                if not remarks:
                    continue


                context.append(f"\n    {category}")

                for remark in remarks:
                    context.append(f"        • {remark}")

        context.append("")


            # Hypotheses

        context.append("Pending Questions:")

        if self.hypotheses:
            for hypothesis in self.hypotheses:
                context.append(f"- {hypothesis}")

        else:
            context.append("- None")


        context.append("")

            # Completed Sections

        context.append("Completed Sections:")

        if self.completed_sections:
            for section in sorted(self.completed_sections):
                context.append(f"- {section}")

        else:
            context.append("- None")

        return "\n".join(context)

    def update_lost_business(self, fact):

        for category, stats in fact["statistics"].items():
            self.lost_business["categories"][category] = stats

        for category, remarks in fact["examples"].items():

            if category not in self.lost_business["examples"]:
                self.lost_business["examples"][category] = []

            existing = {
                r.lower().strip()
                for r in self.lost_business["examples"][category]
            }

            for remark in remarks:

                key = remark.lower().strip()

                if key not in existing:
                    self.lost_business["examples"][category].append(remark)
                    existing.add(key)

            # Keep only the first 3 unique examples
            self.lost_business["examples"][category] = \
                self.lost_business["examples"][category][:3]