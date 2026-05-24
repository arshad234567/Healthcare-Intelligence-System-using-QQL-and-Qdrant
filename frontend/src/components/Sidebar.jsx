import {
  HeartPulse,
  Activity,
  ShieldCheck,
  Stethoscope
} from "lucide-react"

export default function Sidebar() {

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-sky-100 p-6 h-fit sticky top-6">

      <div className="flex items-center gap-3 mb-6">

        <div className="bg-sky-100 p-3 rounded-2xl">
          <HeartPulse className="w-8 h-8 text-sky-700" />
        </div>

        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            MedAI Assistant
          </h1>

          <p className="text-gray-500 text-sm">
            Agentic Healthcare RAG
          </p>
        </div>
      </div>

      <div className="space-y-5">

        <div className="bg-sky-50 rounded-2xl p-4 border border-sky-100">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="text-sky-700 w-5 h-5" />
            <h2 className="font-semibold text-gray-800">
              AI Retrieval
            </h2>
          </div>

          <p className="text-sm text-gray-600 leading-6">
            Uses semantic vector retrieval with Qdrant.
          </p>
        </div>

        <div className="bg-sky-50 rounded-2xl p-4 border border-sky-100">
          <div className="flex items-center gap-3 mb-2">
            <ShieldCheck className="text-sky-700 w-5 h-5" />
            <h2 className="font-semibold text-gray-800">
              Safety Grounding
            </h2>
          </div>

          <p className="text-sm text-gray-600 leading-6">
            Context-grounded healthcare responses.
          </p>
        </div>

        <div className="bg-sky-50 rounded-2xl p-4 border border-sky-100">
          <div className="flex items-center gap-3 mb-2">
            <Stethoscope className="text-sky-700 w-5 h-5" />
            <h2 className="font-semibold text-gray-800">
              Medical Context
            </h2>
          </div>

          <p className="text-sm text-gray-600 leading-6">
            Intelligent healthcare reasoning system.
          </p>
        </div>
      </div>
    </div>
  )
}