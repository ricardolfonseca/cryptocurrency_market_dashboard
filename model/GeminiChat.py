import google.generativeai as genai
import streamlit as st

class GeminiChat:
    """Manages Gemini model selection, context building, and response generation."""

    def __init__(self, api_key=None):
        """Initialize with API key. If none provided, try to get from secrets."""
        if api_key:
            genai.configure(api_key=api_key)
        else:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            except KeyError:
                st.error("Gemini API key not found in secrets.")
        self.model_name = self._get_best_model()

    def _get_best_model(self):
        """
        Return the most suitable model name for chat.
        Priority: gemini-2.5-flash, gemini-flash-latest, any flash model, any chat model.
        """
        try:
            models = genai.list_models()
            chat_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
            chat_model_names = [m.name.replace('models/', '') for m in chat_models]

            if 'gemini-2.5-flash' in chat_model_names:
                return 'gemini-2.5-flash'
            if 'gemini-flash-latest' in chat_model_names:
                return 'gemini-flash-latest'

            flash_models = [name for name in chat_model_names if 'flash' in name.lower()]
            if flash_models:
                return flash_models[0]
            if chat_model_names:
                return chat_model_names[0]
        except Exception as e:
            st.warning(f"Error listing models: {e}")

        # Fallback
        fallback_models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']
        for model in fallback_models:
            try:
                genai.get_model(f"models/{model}")
                return model
            except:
                continue
        return None

    def _build_market_context(self, live_data, currency="USD"):
        """Create a detailed context string with currency information."""
        if live_data is None or live_data.empty:
            return "No market data available."

        symbols = {"usd": "$", "eur": "€", "gbp": "£", "USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(currency.upper(), "$")

        cols = ['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']
        available_cols = [col for col in cols if col in live_data.columns]
        df_display = live_data[available_cols].copy()

        if 'current_price' in df_display.columns:
            df_display['current_price'] = df_display['current_price'].apply(lambda x: f"{symbol}{x:,.2f}")
        if 'market_cap' in df_display.columns:
            df_display['market_cap'] = df_display['market_cap'].apply(lambda x: f"{symbol}{x:,.0f}")
        if 'total_volume' in df_display.columns:
            df_display['total_volume'] = df_display['total_volume'].apply(lambda x: f"{symbol}{x:,.0f}")
        if 'price_change_percentage_24h' in df_display.columns:
            df_display['price_change_percentage_24h'] = df_display['price_change_percentage_24h'].round(2).apply(lambda x: f"{x}%")

        context = f"CURRENT MARKET DATA (top 10 by market cap) – All prices are in **{currency.upper()}**.\n\n"
        context += df_display.to_string(index=False)
        context += "\n\nIMPORTANT: The data above is only available in the selected currency. If the user asks for prices in a different currency, politely explain that the dashboard only displays data in the current currency and suggest they change it using the sidebar dropdown. Do NOT attempt conversions."
        return context

    def get_response(self, question, live_data=None, currency="USD"):
        """Generate a response from Gemini."""
        if not self.model_name:
            return "Sorry, no Gemini model is available at the moment."

        try:
            model = genai.GenerativeModel(self.model_name)
            context = self._build_market_context(live_data, currency) if live_data is not None else "No market data provided."
            full_prompt = (
                f"{context}\n\n"
                f"User question: {question}\n\n"
                "Instructions:\n"
                "- Answer based on the provided data and your general knowledge about cryptocurrencies.\n"
                f"- The data above is in **{currency.upper()}**. If the user asks for prices in another currency, DO NOT perform any conversion. Instead, politely explain that the dashboard only displays prices in the selected currency and advise them to change the currency in the sidebar settings.\n"
                "- If the question is unclear, ask for clarification.\n"
                "- Use the data to support your answers, and indicate when you are using general knowledge."
            )
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"