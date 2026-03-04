'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, Calendar, Activity, AlertTriangle, Info, CheckCircle, ShieldUser, ChevronDown, ChevronUp, ShieldCheck } from 'lucide-react';

const conditionInsights: Record<string, string> = {
  heart_disease: "Score driven primarily by baseline cardiovascular indicators. Maintain regular monitoring of blood pressure.",
  diabetes: "Fasting blood glucose and lifestyle factors indicate this level of concern. Dietary modifications may be required.",
  parkinsons: "Based on age and available neurological indicators. Ongoing monitoring of motor functions is recommended.",
  breast_cancer: "Evaluated based on standard health metrics. Regular screenings and self-examinations are your strongest preventative measure."
};

const preventionTips: Record<string, { prevention: string, mitigation: string }> = {
  heart_disease: {
    prevention: "Adopt a heart-healthy diet rich in fruits, vegetables, and whole grains. Engage in at least 150 minutes of moderate aerobic activity weekly and manage stress effectively.",
    mitigation: "Monitor blood pressure and cholesterol levels regularly. Adhere strictly to prescribed medications and consider cardiac rehabilitation if directed by a physician."
  },
  diabetes: {
    prevention: "Maintain a healthy weight by reducing refined carbohydrate intake and staying physically active. Ensure adequate fiber intake to help regulate blood sugar spikes.",
    mitigation: "Consistently track blood glucose levels, adhere to insulin or oral medications as prescribed, and attend regular foot and eye examinations to prevent complications."
  },
  parkinsons: {
    prevention: "While direct prevention is unclear, regular physical exercise (especially aerobic) and a diet rich in antioxidants (like the Mediterranean diet) may offer protective benefits.",
    mitigation: "Engage in physical therapy, occupational therapy, and specialized speech therapy. Strictly adhere to dopamine-regulating medications under a neurologist's care."
  },
  breast_cancer: {
    prevention: "Limit alcohol consumption, maintain a healthy weight, and stay physically active. Consider genetic counseling if there is a strong family history and discuss risk-reducing strategies.",
    mitigation: "Follow through with prescribed treatments (surgery, radiation, chemotherapy). Attend regular follow-up screenings, join support groups, and monitor for recurrence."
  }
};

const defaultInsight = "Evaluated based on the answers provided in your recent lifestyle and health assessment.";
const defaultTips = {
  prevention: "Maintain a balanced diet, exercise regularly, and avoid smoking and excessive alcohol consumption.",
  mitigation: "Consult your primary care physician for a personalized management plan and attend all recommended follow-ups."
};

export default function Predict() {
  const [results, setResults] = useState<Record<string, number[]> | null>(null);
  const [expandedCard, setExpandedCard] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const stored = sessionStorage.getItem('predictionResult');
    if (!stored) {
      router.push('/');
      return;
    }
    setResults(JSON.parse(stored));
  }, [router]);

  if (!results) {
    return (
      <div className="container min-h-screen flex items-center justify-center">
        <div className="loading text-amber-600 font-medium tracking-wide">Generating Medical Report...</div>
      </div>
    );
  }

  const formatString = (str: string) => str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

  // Current Date
  const today = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <div className="w-full px-6 py-10 md:px-12 md:py-16 lg:px-24 mx-auto relative max-w-[1600px]">

        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-stone-200 pb-8 mb-8">
          <div className="flex items-center gap-3 mb-6 md:mb-0">
            <ShieldUser className="w-8 h-8 text-amber-600" />
            <span className="text-2xl font-black text-amber-600 tracking-tight">RiskVision</span>
          </div>
          <div className="text-right">
            <div className="inline-block bg-amber-50 text-amber-600 px-4 py-1 rounded-full text-xs font-bold tracking-widest uppercase mb-2">
              Confidential Medical Report
            </div>
            <p className="text-stone-500 text-sm font-medium">Report ID: #RV-{Math.floor(1000 + Math.random() * 9000)}-{new Date().getFullYear()}</p>
          </div>
        </div>

        {/* Title & Patient Info */}
        <div className="flex flex-col md:flex-row justify-between gap-8 mb-12">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-extrabold text-stone-900 mb-2 leading-tight">Health Assessment<br />Summary</h1>
            <p className="text-stone-500 text-base">Comprehensive chronic condition risk analysis</p>
          </div>

          <div className="bg-stone-50 border border-stone-100 rounded-xl p-6 flex-1 max-w-sm">
            <div className="grid grid-cols-2 gap-y-3 text-sm">
              <div className="text-stone-500 font-medium">Patient Name:</div>
              <div className="font-bold text-stone-900 text-right border-b border-stone-200 border-dashed pb-1"></div>

              <div className="text-stone-500 font-medium">Date of Birth:</div>
              <div className="font-bold text-stone-900 text-right border-b border-stone-200 border-dashed pb-1"></div>

              <div className="text-stone-500 font-medium">Assessment Date:</div>
              <div className="font-bold text-stone-900 text-right">{today}</div>
            </div>
          </div>
        </div>

        {/* Condition Risk Analysis Section */}
        <div className="mb-14">
          <div className="flex items-center gap-2 mb-6 text-stone-700 tracking-wide font-bold uppercase text-sm">
            <Activity className="w-5 h-5 text-amber-500" />
            Condition Risk Analysis
          </div>

          <div className="grid grid-cols-2 gap-4">
            {Object.entries(results).map(([disease, prediction]) => {
              const riskValue = prediction[0] || 0;
              const isHighRisk = riskValue >= 50;
              const isModerateRisk = riskValue >= 20 && riskValue < 50;
              const isExpanded = expandedCard === disease;
              const tips = preventionTips[disease] || defaultTips;

              // Determine tag colors based on threshold
              let riskLevel = "Low Risk";
              let colorClass = "text-emerald-600";
              let bgClass = "bg-emerald-100";

              if (isHighRisk) {
                riskLevel = "High Risk";
                colorClass = "text-red-600";
                bgClass = "bg-red-100";
              } else if (isModerateRisk) {
                riskLevel = "Moderate Risk";
                colorClass = "text-amber-600";
                bgClass = "bg-amber-100";
              }

              return (
                <div>
                  <Card key={disease} className="overflow-hidden border border-stone-200 shadow-sm flex flex-col transition-all duration-300">
                    <div className="flex flex-col md:flex-row items-stretch">
                      <div className="md:w-48 w-full p-6 md:p-8 flex flex-col items-center justify-center border-b md:border-b-0 md:border-r border-stone-100 bg-stone-50/50">
                        <div className={`text-4xl md:text-5xl font-black tracking-tighter ${colorClass} mb-2`}>
                          {Math.round(riskValue)}<span className="text-2xl">%</span>
                        </div>
                        <div className={`px-3 py-1 rounded text-[10px] font-bold tracking-widest uppercase ${bgClass} ${colorClass}`}>
                          {riskLevel}
                        </div>
                      </div>

                      <div className="flex-1 p-6 md:p-8 flex flex-col justify-center">
                        <h3 className="text-xl font-bold text-stone-800 capitalize mb-2">{formatString(disease)}</h3>
                        <p className="text-stone-600 text-sm leading-relaxed mb-4">
                          {conditionInsights[disease] || defaultInsight}
                        </p>

                        <div className="mt-auto pt-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setExpandedCard(isExpanded ? null : disease)}
                            className="text-amber-600 border-amber-200 hover:bg-amber-50 hover:text-amber-700 font-semibold"
                          >
                            {isExpanded ? (
                              <><ChevronUp className="w-4 h-4 mr-1" /> Hide Prevention Strategies</>
                            ) : (
                              <><ChevronDown className="w-4 h-4 mr-1" /> View Prevention Strategies</>
                            )}
                          </Button>
                        </div>
                      </div>
                    </div>

                    {/* Expandable Mitigation Section */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3, ease: "easeInOut" }}
                          className="border-t border-stone-100"
                        >
                          <div className="p-6 md:p-8 bg-[#fffcf3] grid grid-cols-1 md:grid-cols-2 gap-8 border-l-4 border-amber-400">
                            <div>
                              <div className="flex items-center gap-2 mb-3">
                                <ShieldCheck className="w-5 h-5 text-amber-600" />
                                <h4 className="font-bold text-stone-800 text-lg">Prevention Strategies</h4>
                              </div>
                              <p className="text-stone-600 leading-relaxed text-sm md:text-base">
                                {tips.prevention}
                              </p>
                            </div>
                            <div>
                              <div className="flex items-center gap-2 mb-3">
                                <Activity className="w-5 h-5 text-amber-600" />
                                <h4 className="font-bold text-stone-800 text-lg">Mitigation & Action</h4>
                              </div>
                              <p className="text-stone-600 leading-relaxed text-sm md:text-base">
                                {tips.mitigation}
                              </p>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </Card>
                </div>
              );
            })}
          </div>
        </div>

        {/* Key Findings Placeholder Section */}
        <div className="mb-16">
          <div className="flex items-center gap-2 mb-6 text-stone-700 tracking-wide font-bold uppercase text-sm">
            <Info className="w-5 h-5 text-amber-500" />
            Key Findings & Contributing Factors
          </div>

          <div className="bg-stone-50 rounded-xl p-6 md:p-8 border border-stone-100 space-y-6">
            <div className="flex items-start gap-4">
              <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-stone-800 text-sm mb-1">General Indicators</h4>
                <p className="text-stone-500 text-xs md:text-sm">Metrics were extrapolated from your self-reported inputs. Clinical verification is required.</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-stone-800 text-sm mb-1">Protective Factors</h4>
                <p className="text-stone-500 text-xs md:text-sm">Active lifestyle choices and regular clinical screenings serve as your strongest defense against disease progression.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Next Steps */}
        <div className="text-center pt-12 mt-4 border-t border-stone-100 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-stone-900 mb-4">Next Steps & Doctor Consultation</h2>
          <p className="text-stone-500 text-sm mb-8 leading-relaxed">
            We recommend sharing this summary with your primary care physician during your next visit. Early intervention through lifestyle changes and potential medical management can significantly lower your long-term risks.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Button className="w-full sm:w-auto bg-amber-600 hover:bg-amber-700 text-white shadow-xl shadow-amber-600/20 font-bold px-8 py-6 rounded-lg">
              <Download className="w-5 h-5 mr-2" /> Download PDF Report
            </Button>
            <Button variant="outline" className="w-full sm:w-auto border-2 border-stone-200 font-bold px-8 py-6 rounded-lg text-stone-700 hover:bg-stone-50">
              <Calendar className="w-5 h-5 mr-2 text-stone-400" /> Schedule Physician Call
            </Button>
          </div>

          <p className="text-[10px] text-stone-400 italic">
            * This report is for informational purposes only and does not constitute a formal medical diagnosis.
            <br /><br />
            RISKVISION DIGITAL ASSESSMENT • POWERED BY MEDICAL INSIGHTS ENGINE V1.2
          </p>
        </div>

      </div>
    </div>
  );
}
