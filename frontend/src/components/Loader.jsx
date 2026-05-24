import { Loader2 } from "lucide-react"

export default function Loader() {

  return (

    <div className="bg-white rounded-3xl shadow-xl border border-sky-100 p-8 flex items-center justify-center gap-4">

      <Loader2 className="w-8 h-8 animate-spin text-sky-700" />

      <p className="text-lg font-medium text-gray-700">
        Generating healthcare response...
      </p>

    </div>
  )
}