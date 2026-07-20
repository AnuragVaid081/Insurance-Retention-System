import json
import logging

from config import LLMConfig
from exceptions import LLMResponseError
from schemas import(
    PolicyContext,
    PolicyAnalysisResponse,
    PredictionExplanation,
    Recommendation,
    RemarkAdjustment
)

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    Validates and parses the raw json response returned by the LLM.
    """

    @staticmethod
    def parse(
        response: str,
        context: PolicyContext
    ) -> PolicyAnalysisResponse:
        
        logger.info("Parsing LLM Response.")

        data = ResponseParser._load_json(response)

        prediction = ResponseParser._parse_prediction(data)

        adjustments = ResponseParser._parse_adjustments(
            data,
            context
        )

        recommendation = ResponseParser._parse_recommendation(data)

        logger.info("LLM response parsed succesfully.")

        return PolicyAnalysisResponse(

            prediction_explanation = prediction,
            
            remark_adjustments = adjustments,
            
            overall_summary = data.get("overall_summary",""),
            
            recommendation = recommendation
        )
    

    # @staticmethod
    # def _load_json(response: str) -> dict:
    #     """
    #     Convert the raw JSON string into a dictionary
    #     """
    #     with open("llm_response.json","w", encoding = "utf-8") as f:

    #         try:
    #             return json.loads(response)
            
    #         except json.JSONDecodeError as e:
    #             print(f"JSON error at line {e.lineno}, column {e.colno}")
    #             raise LLMResponseError(
    #                 "Invalid JSON returned by LLM"
    #             )from e
    @staticmethod
    def _load_json(response: str) -> dict:
        print("=" * 100)
        print(response)
        print("=" * 100)

        with open("llm_response.txt", "w", encoding="utf-8") as f:
            f.write(response)

        try:
            return json.loads(response)

        except json.JSONDecodeError as e:
            print(f"\nJSON error at line {e.lineno}, column {e.colno}")
            print(f"Character position: {e.pos}")
            raise LLMResponseError(
                "Invalid JSON returned by LLM"
            ) from e



    @staticmethod
    def _parse_prediction(data: dict) -> PredictionExplanation:

        explanation = data.get(
            "prediction_explanation",
            {}
        )

        return PredictionExplanation(

            summary = explanation.get(
                "summary",
                ""
            ),

            supporting_factors = explanation.get(
                "supporting_factors",
                []
            ),

            risk_factors = explanation.get(
                "risk_factors",
                []
            )

        )

    
    @staticmethod
    def _parse_adjustments(
        data: dict,
        context: PolicyContext
    ) -> list[RemarkAdjustment]:
        """
        Parse all remark adjustments.
        """

        parsed = []

        adjustments = data.get(
            "remark_adjustments",
            []
        )

        for adjustment in adjustments:

            try:

                remark_index = adjustment.get(
                    "remark_index",
                    -1
                )

                if (
                    remark_index < 0 or
                    remark_index >= len(context.remarks)
                ):
                    raise LLMResponseError(
                        f"Invalid remark index: {remark_index}"
                    )

                ResponseParser._validate_evidence(
                    adjustment.get("evidence", []),
                    context.remarks[remark_index].text
                )

                parsed.append(

                    RemarkAdjustment(

                        remark_index= remark_index,

                        remark = context.remarks[remark_index].text,

                        impact=ResponseParser._normalize_impact(
                            adjustment.get(
                                "impact",
                                "Neutral"
                            )
                        ),

                        adjustment=ResponseParser._normalize_adjustment(
                            adjustment.get(
                                "adjustment",
                                0
                            )
                        ),

                        confidence=ResponseParser._normalize_confidence(
                            adjustment.get(
                                "confidence",
                                "Medium"
                            )
                        ),

                        reasoning=adjustment.get(
                            "reasoning",
                            ""
                        ),

                        evidence=adjustment.get(
                            "evidence",
                            []
                        )

                    )

                )

            except LLMResponseError as e:

                logger.warning(
                "Skipping remark adjustment (index=%s): %s",
                adjustment.get("remark_index", "unknown"),
                e
                )

                continue
        return parsed

    @staticmethod
    def _normalize_adjustment(
        value
    ) -> int:
        """
        Convert the adjustment into a valid integer within the 
        configured limits
        """

        try:

            value = int(value)

        except (TypeError,ValueError):
            value = 0

        return max(
            LLMConfig.MIN_ADJUSTMENT,
            min(value,LLMConfig.MAX_ADJUSTMENT)
        )
    
    @staticmethod
    def _normalize_confidence(
        value: str
    ) -> str:
        
        value = str(value).strip().lower()

        mapping = {
            
            "low": "Low",
            
            "medium": "Medium",

            "high": "High"
        }

        return mapping.get(
            value,
            "Medium"
        )
    

    @staticmethod
    def _normalize_impact(
        value: str
    ) -> str:
        
        value = str(value).strip().lower()

        mapping = {

            "positive": "Positive",

            "neutral": "Neutral",

            "negative": "Negative"
        }

        return mapping.get(
            value,
            "Neutral"
        )
    
    @staticmethod
    def _validate_evidence(
        evidence: list[str],
        remark: str
    ) -> None:
        """
        Ensure every evidence phrase exists inside the remark.
        """

        remark = remark.lower()

        for phrase in evidence:

            if phrase.lower() not in remark:

                raise LLMResponseError(
                    f"Evidence '{phrase}' not found in remark."
                )
            
    @staticmethod
    def _parse_recommendation(
        data: dict
    ) -> Recommendation:
        """
        Parse and validate the recommendation section
        """

        recommendation = data.get("recommendation",{})

        priority = str(
            recommendation.get("priority","Medium")
        ).strip().capitalize()

        if priority not in ("Low", "Medium", "High"):
            priority = "Medium"

        return Recommendation(
            priority= priority,
            action= recommendation.get(
                "action",
                ""
            )
        )