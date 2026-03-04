'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle2, Circle } from 'lucide-react';

const diseaseImages: Record<string, string> = {
  heart_disease: "/heart.png",
  diabetes: "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=800&q=80",
  parkinsons: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=800&q=80",
  breast_cancer: "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&q=80",
};

const defaultImage = "https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=800&q=80";

export default function Home() {
  const [selectedDiseases, setSelectedDiseases] = useState<string[]>([]);
  const router = useRouter();

  const { data: diseasesData, isLoading, isError } = useQuery({
    queryKey: ['diseases'],
    queryFn: async () => {
      const res = await fetch('http://localhost:5000/api/diseases');
      if (!res.ok) throw new Error('Failed to fetch');
      return res.json();
    }
  });

  const diseases: string[] = diseasesData?.diseases || [];

  const toggleDisease = (disease: string) => {
    if (selectedDiseases.includes(disease)) {
      setSelectedDiseases(selectedDiseases.filter(d => d !== disease));
    } else {
      setSelectedDiseases([...selectedDiseases, disease]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedDiseases.length === 0) {
      alert("Please select at least one assessment");
      return;
    }
    sessionStorage.setItem('selectedDiseases', JSON.stringify(selectedDiseases));
    router.push('/questioneres');
  };

  const formatString = (str: string) => str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <div className="container min-h-screen py-16 flex items-center justify-center">
      <div className="min-w-[50vw]">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-extrabold tracking-tight text-stone-900 mb-4">RiskVision Health Assessments</h1>
          <p className="text-xl text-stone-500 max-w-2xl mx-auto">
            Select the health conditions you wish to be evaluated for to start your personalized risk screening.
          </p>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="loading text-amber-600 font-medium text-lg flex items-center">Loading assessments...</div>
          </div>
        ) : isError ? (
          <div className="text-red-500 text-center py-10 font-medium bg-red-50 rounded-xl border border-red-200 p-8">
            Failed to load diseases. Make sure the backend API is running.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-10">
              {diseases.map(disease => {
                const isSelected = selectedDiseases.includes(disease);
                const imageUrl = diseaseImages[disease] || defaultImage;

                return (
                  <div
                    key={disease}
                    className={`relative flex flex-col cursor-pointer rounded-2xl border-2 overflow-hidden shadow-sm transition-all duration-300 hover:-translate-y-1 group bg-white ${isSelected
                      ? 'border-amber-600 ring-2 ring-amber-600/20 shadow-amber-600/10 shadow-xl'
                      : 'border-stone-200 hover:border-amber-400 hover:shadow-xl'
                      }`}
                    onClick={() => toggleDisease(disease)}
                  >
                    <div className="h-64 sm:h-72 w-full relative overflow-hidden bg-stone-100">
                      <img
                        src={imageUrl}
                        alt={formatString(disease)}
                        className={`w-full h-full object-cover transition-transform duration-700 ease-in-out ${isSelected ? 'scale-105' : 'group-hover:scale-105'}`}
                      />
                      <div className="absolute inset-0 bg-linear-to-t from-black/50 to-transparent" />
                    </div>

                    <div className={`p-5 flex-1 flex flex-col justify-center transition-colors ${isSelected ? 'bg-amber-50/30' : ''}`}>
                      <h3 className="font-bold text-xl text-stone-800 capitalize mb-1">
                        {formatString(disease)}
                      </h3>
                      <p className="text-sm text-stone-500 font-medium">Risk Screening</p>
                    </div>

                    {/* Hidden input for semantics */}
                    <input
                      type="checkbox"
                      value={disease}
                      checked={isSelected}
                      onChange={() => { }}
                      className="hidden"
                    />
                  </div>
                );
              })}
            </div>

            <div className="flex justify-center border-t border-stone-200 pt-10">
              <Button
                type="submit"
                size="lg"
                disabled={selectedDiseases.length === 0}
                className="w-full sm:w-auto px-12 py-7 text-xl font-bold text-white bg-amber-600 hover:bg-amber-700 shadow-xl shadow-amber-600/20 rounded-full transition-all disabled:opacity-50 disabled:hover:scale-100 active:scale-95"
              >
                Begin Questionnaire
              </Button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
