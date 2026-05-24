import { HeartPulse } from "lucide-react"

export default function ResponseCard({ response }) {

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-sky-100 p-8">

      <div className="flex items-center gap-3 mb-6">

        <div className="bg-sky-100 p-3 rounded-2xl">
          <HeartPulse className="text-sky-700" />
        </div>

        <h2 className="text-3xl font-bold text-gray-900">
          AI Healthcare Response
        </h2>

      </div>

      <div className="bg-sky-50 border border-sky-100 rounded-3xl p-6 whitespace-pre-wrap leading-8 text-gray-700 text-[15px]">

        {response}

      </div>
    </div>
  )
}