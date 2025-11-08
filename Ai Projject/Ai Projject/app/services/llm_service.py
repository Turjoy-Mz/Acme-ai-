"""Mock LLM service for generating responses."""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MockLLMService:
    """Mock LLM service for generating healthcare responses."""
    
    # Mock medical guidelines database
    MEDICAL_RESPONSES = {
        "en": {
            "diabetes": """Based on recent medical guidelines:

**Type 2 Diabetes Management Recommendations:**
1. **Lifestyle Modifications**: Regular exercise (150 min/week), Mediterranean diet
2. **Pharmacological Intervention**: Start with Metformin if A1C > 7%
3. **Monitoring**: Check HbA1c every 3 months until stable, then every 6 months
4. **Comorbidities**: Manage hypertension (target <130/80) and dyslipidemia
5. **Prevention**: Screen for nephropathy, neuropathy, and retinopathy annually

Latest 2024-2025 evidence emphasizes early GLP-1 receptor agonist use for patients with cardiovascular disease or chronic kidney disease.""",
            
            "hypertension": """**Hypertension Management Guidelines:**
1. **Initial Assessment**: Measure BP in both arms; consider 24-hour ambulatory monitoring
2. **Lifestyle Changes**: DASH diet, sodium reduction, weight loss, exercise
3. **Pharmacotherapy Initiation**: Start at Stage 1 HTN if high cardiovascular risk
4. **Target Goals**: <130/80 mmHg for most patients
5. **Follow-up**: Adjust medications every 1 month until controlled
6. **Special Populations**: Consider individual factors (age, comorbidities, medications)

Current evidence supports combination therapy for most hypertensive patients.""",
            
            "default": """Healthcare recommendations based on current evidence:

The response is generated based on retrieved medical documents and latest clinical guidelines. Always consult with healthcare professionals for personalized medical advice.

Key Considerations:
- Evidence-based practice guidelines (2024-2025)
- Individual patient factors and comorbidities
- Regular monitoring and follow-up
- Patient education and lifestyle modifications"""
        },
        "ja": {
            "diabetes": """最新の医学ガイドラインに基づく糖尿病管理：

**2型糖尿病管理の推奨事項：**
1. **生活様式の改善**: 週150分の運動、地中海式食
2. **薬物療法**: HbA1c > 7%の場合、メトホルミンで開始
3. **モニタリング**: 安定するまで3ヶ月ごと、その後6ヶ月ごとにHbA1cを確認
4. **併存疾患**: 高血圧（目標<130/80）と脂質異常症を管理
5. **予防**: 腎障害、神経障害、網膜症を毎年スクリーニング

2024-2025の最新エビデンスは、心血管疾患または慢性腎臓病の患者へのGLP-1受容体作動薬の早期使用を強調しています。""",
            
            "hypertension": """**高血圧管理ガイドライン：**
1. **初期評価**: 両腕で血圧を測定、24時間外来血圧モニタリングを検討
2. **生活様式の改善**: DASH食、塩分制限、体重減少、運動
3. **薬物療法の開始**: 高心血管リスクの場合、第1段階HTNで開始
4. **目標値**: ほとんどの患者で<130/80 mmHg
5. **追跡**: 管理されるまで毎月投薬を調整
6. **特殊集団**: 個別の要因（年齢、併存疾患、薬物）を考慮

現在のエビデンスはほとんどの高血圧患者への併用療法をサポートしています。""",
            
            "default": """医学的根拠に基づいたヘルスケアの推奨事項：

この応答は、検索された医学文書と最新の臨床ガイドラインに基づいて生成されます。個別の医学的アドバイスについては、必ずヘルスケアプロフェッショナルに相談してください。

重要な考慮事項：
- 根拠に基づいた診療ガイドライン（2024-2025）
- 患者個別の要因と併存疾患
- 定期的なモニタリングと追跡
- 患者教育とライフスタイルの改善"""
        }
    }
    
    @staticmethod
    def generate_response(
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        language: str = "en"
    ) -> str:
        """
        Generate a mock LLM response based on query and retrieved documents.
        
        Args:
            query: User query
            retrieved_documents: List of retrieved documents
            language: Output language
        
        Returns:
            Generated response text
        """
        # Determine response type based on query keywords
        query_lower = query.lower()
        response_type = "default"
        
        if any(word in query_lower for word in ["diabetes", "blood sugar", "glucose"]):
            response_type = "diabetes"
        elif any(word in query_lower for word in ["hypertension", "blood pressure", "high bp"]):
            response_type = "hypertension"
        
        # Get appropriate response
        responses = MockLLMService.MEDICAL_RESPONSES.get(language, MockLLMService.MEDICAL_RESPONSES["en"])
        response = responses.get(response_type, responses["default"])
        
        # Include document references in response
        if retrieved_documents:
            response += f"\n\n**Referenced Medical Sources:** {len(retrieved_documents)} document(s) analyzed."
        
        return response
