'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft, ArrowRight, CheckCircle2, Circle, Info, Activity } from 'lucide-react';

import { API_ROUTES } from '@/lib/api-routes';

type Feature = {
  label: string;
  desc?: string;
  options?: string[];
  formula?: string;
};

type QuestionGroup = {
  [category: string]: {
    [featureName: string]: Feature;
  }
};

export default function Questioneres() {
  const [selectedDiseases, setSelectedDiseases] = useState<string[]>([]);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [currentStep, setCurrentStep] = useState(0);
  const router = useRouter();

  useEffect(() => {
    const stored = sessionStorage.getItem('selectedDiseases');
    if (!stored) {
      router.push('/');
      return;
    }
    setSelectedDiseases(JSON.parse(stored));
  }, [router]);

  const { data: questionGroup, isLoading, isError } = useQuery({
    queryKey: ['questions', selectedDiseases],
    queryFn: async () => {
      const res = await fetch(API_ROUTES.QUESTIONNAIRE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selectedDiseases })
      });
      if (!res.ok) throw new Error('Failed to fetch questions');
      const data = await res.json();
      return data.question_group as QuestionGroup;
    },
    enabled: selectedDiseases.length > 0
  });

  const predictMutation = useMutation({
    mutationFn: async (payload: { selectedDiseases: string[], form_data: Record<string, string> }) => {
      const res = await fetch(API_ROUTES.PREDICT_RISK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Risk calculation failed');
      return res.json();
    },
    onSuccess: (data) => {
      if (data.error) {
        alert('Error: ' + data.error);
        return;
      }
      sessionStorage.setItem('predictionResult', JSON.stringify(data.diseases_risk));
      router.push('/predict');
    },
    onError: (err) => {
      console.error(err);
      alert("An error occurred while evaluating risk.");
    }
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const formatString = (str: string) => str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

  if (isLoading || !questionGroup) {
    return (
      <div className="container min-h-screen flex items-center justify-center">
        <div className="loading flex items-center text-amber-600 font-medium">Preparing your assessment...</div>
      </div>
    );
  }

  const groupEntries = Object.entries(questionGroup).filter(([_, features]) =>
    Object.values(features).some(f => !f.formula)
  );

  const totalSteps = groupEntries.length;

  if (totalSteps === 0) {
    return (
      <div className="container min-h-screen flex items-center justify-center">
        <Card className="p-8 text-center text-red-500">Failed to load valid questions.</Card>
      </div>
    );
  }

  const [currentGroupName, currentFeatures] = groupEntries[currentStep];

  // Logic to separate "select" (tiles) and "input" (biometrics)
  const selectFeatures = Object.entries(currentFeatures).filter(([_, f]) => f.options && !f.formula);
  const numericFeatures = Object.entries(currentFeatures).filter(([_, f]) => !f.options && !f.formula);

  const handleNextSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      predictMutation.mutate({ selectedDiseases, form_data: formData });
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    } else {
      router.push('/');
    }
  };

  const progressPercentage = ((currentStep + 1) / totalSteps) * 100;

  // Ensure all select-tiles are filled before allowing Next
  const isNextDisabled = predictMutation.isPending ||
    (selectFeatures.length > 0 && !selectFeatures.every(([k]) => formData[k]));

  return (
    <div className="min-h-screen bg-stone-50 py-10 px-4 md:px-0 font-sans flex flex-col items-center justify-center">
      <div className="w-full max-w-[40vw] mx-auto">
        {/* Progress Header */}
        <div className="flex justify-between items-end mb-3">
          <div>
            <h1 className="text-2xl font-bold text-stone-900 capitalize">{formatString(currentGroupName)} Assessment</h1>
            <p className="text-sm font-medium text-stone-500 mt-1">Health Risk Module</p>
          </div>
          <div className="text-base font-bold text-amber-600">
            Question {currentStep + 1} <span className="text-stone-400 font-medium">/ {totalSteps}</span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-stone-200 h-2.5 rounded-full mb-8 overflow-hidden">
          <div
            className="h-full bg-amber-600 transition-all duration-500 ease-out"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>

        {/* Main Interface Card */}
        <Card className="bg-white shadow-xl shadow-stone-200/50 border-0 rounded-2xl mb-8 overflow-hidden pt-0">
          {/* Header Image Placeholder equivalent to the cactus */}
          <div className="h-48 w-full relative bg-stone-100">
            <img
              src="https://images.unsplash.com/photo-1550831107-1553da8c8464?q=80&w=2000&auto=format&fit=crop"
              alt="Category Banner"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent" />
          </div>

          <CardContent className="px-8 py-4 animate-in slide-in-from-bottom-2 duration-300">
            <form onSubmit={handleNextSubmit} id="assessment-form">

              {/* Tile Selection Features */}
              {selectFeatures.map(([fname, f]) => (
                <div key={fname} className="mb-10 last:mb-0">
                  <h2 className="text-3xl font-bold text-stone-900 mb-4 leading-tight">{f.label}</h2>
                  {f.desc && <p className="text-stone-500 text-lg mb-8">{f.desc}</p>}

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {f.options!.map(opt => {
                      const isSelected = formData[fname] === opt;
                      return (
                        <div
                          key={opt}
                          onClick={() => handleSelectChange(fname, opt)}
                          className={`relative flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${isSelected
                            ? 'border-amber-600 bg-amber-50/50 text-amber-900 ring-2 ring-amber-600/10'
                            : 'border-stone-200 bg-white hover:border-amber-300 hover:bg-stone-50 text-stone-700'
                            }`}
                        >
                          <div className="flex-1 font-medium text-base">{opt}</div>
                          {isSelected ? (
                            <CheckCircle2 className="w-5 h-5 text-amber-600 flex-shrink-0 ml-3" />
                          ) : (
                            <Circle className="w-5 h-5 text-stone-300 flex-shrink-0 ml-3" />
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}

              {/* Optional/Secondary Numeric Features */}
              {numericFeatures.length > 0 && (
                <div className="mt-0 pt-0 border-t border-stone-100">
                  <div className="flex items-center gap-2 mb-8">
                    <Activity className="w-6 h-6 text-amber-600" />
                    <h3 className="text-xl font-bold text-stone-900">Optional: Additional Details</h3>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                    {numericFeatures.map(([fname, f]) => (
                      <div key={fname} className="flex flex-col gap-3">
                        <Label className="text-base font-semibold text-stone-600">{f.label}</Label>
                        <Input
                          type="number"
                          step="0.01"
                          required
                          placeholder={f.desc || 'e.g. 120'}
                          value={formData[fname] || ''}
                          onChange={handleInputChange}
                          name={fname}
                          className="h-14 text-lg border-stone-200 bg-stone-50 focus-visible:ring-amber-600 focus-visible:ring-offset-0 focus-visible:border-amber-600 transition-all rounded-xl placeholder:text-stone-400"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </form>
          </CardContent>
        </Card>

        {/* Footer Navigation matching design */}
        <div className="flex items-center justify-between px-2">
          <Button
            type="button"
            variant="ghost"
            className="text-stone-500 hover:text-stone-900 hover:bg-stone-200/50 px-4 py-6 rounded-xl font-semibold text-lg hidden sm:flex"
            onClick={handleBack}
          >
            <ArrowLeft className="w-5 h-5 mr-2" /> Previous
          </Button>

          <Button
            type="button"
            variant="ghost"
            className="text-stone-500 hover:text-stone-900 hover:bg-stone-200/50 p-4 rounded-xl sm:hidden"
            onClick={handleBack}
          >
            <ArrowLeft className="w-6 h-6" />
          </Button>

          <Button
            type="submit"
            form="assessment-form"
            disabled={isNextDisabled}
            className="bg-amber-600 hover:bg-amber-700 text-white rounded-xl px-8 py-6 text-lg font-bold shadow-xl shadow-amber-600/20 transition-all active:scale-95 disabled:opacity-50"
          >
            {predictMutation.isPending ? 'Calculating...' : (currentStep < totalSteps - 1 ? (
              <>Next Question <ArrowRight className="w-5 h-5 ml-2" /></>
            ) : 'Submit')}
          </Button>
        </div>
      </div>
    </div>
  );
}
