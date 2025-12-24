import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model_to_use = None

    def generate_description(self, title: str) -> str:
        try:
            # 1. 閣下のキーで「本当に使えるモデル」をリストアップする
            if not self.model_to_use:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # 優先順位: 1.5-flash -> 1.5-pro -> 1.0-pro
                for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                    if preferred in available_models:
                        self.model_to_use = preferred
                        break
                if not self.model_to_use:
                    self.model_to_use = available_models[0] # 何でもいいから動くものを掴む

            # 2. 判明した「動くモデル」で生成
            model = genai.GenerativeModel(self.model_to_use)
            response = model.generate_content(f"「{title}」という本を30文字以内で紹介して。")
            return f"[{self.model_to_use}が回答] {response.text.strip()}"

        except Exception as e:
            return f"最終通信エラー: {str(e)}"
