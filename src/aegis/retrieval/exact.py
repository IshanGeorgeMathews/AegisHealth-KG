from typing import Any, Dict, Optional

from aegis.models.retrieval import RetrievalPlan

CARC_CODES = {
    "CO-197": "Precertification/authorization/notification/pre-treatment number missing/invalid.",
    "CO-167": "This (these) diagnosis(es) is (are) not covered, missing, or are invalid.",
    "CO-50": "Non-covered services because this is not deemed a 'medical necessity' by the payer.",
}

CPT_CODES = {
    "95251": "Continuous glucose monitoring — personal, professional interpretation and report.",
    "73721": "Magnetic resonance imaging, joint of lower extremity; without contrast.",
    "90837": "Psychotherapy, 60 minutes with patient.",
}

ICD10_CODES = {
    "E11.9": "Type 2 diabetes mellitus without complications.",
    "M25.561": "Pain in right knee.",
    "F33.1": "Major depressive disorder, recurrent, moderate.",
}


class ExactRetriever:
    def handle_exact_lookup(self, plan: RetrievalPlan) -> Optional[Dict[str, Any]]:
        facts = []
        for c in plan.denial_codes:
            code_upper = c.upper()
            if code_upper in CARC_CODES:
                facts.append(
                    {"code": code_upper, "type": "CARC/DenialCode", "description": CARC_CODES[code_upper]}
                )

        for cpt in plan.cpt_codes:
            if cpt in CPT_CODES:
                facts.append({"code": cpt, "type": "CPTCode", "description": CPT_CODES[cpt]})

        for icd in plan.icd10_codes:
            icd_upper = icd.upper()
            if icd_upper in ICD10_CODES:
                facts.append(
                    {"code": icd_upper, "type": "ICD10Code", "description": ICD10_CODES[icd_upper]}
                )

        if facts:
            return {"facts": facts, "exact_match": True}
        return None
