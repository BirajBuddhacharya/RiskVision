const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const API_ROUTES = {
  DISEASES: `${BASE_URL}/api/diseases`,
  QUESTIONNAIRE: `${BASE_URL}/api/questionere`,
  PREDICT_RISK: `${BASE_URL}/api/predictRisk`,
};
