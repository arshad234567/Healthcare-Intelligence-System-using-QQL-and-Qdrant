export default function ContextCard({

  context,
  index

}) {

  return (
    <div className="border border-sky-100 rounded-3xl p-6 bg-sky-50">

      <div className="flex items-center justify-between mb-6">

        <h3 className="text-xl font-semibold text-gray-800">
          Medical Context {index + 1}
        </h3>

        <span className="bg-sky-700 text-white px-4 py-2 rounded-full text-sm font-medium">
          Score: {context.score}
        </span>

      </div>

      <div className="mb-6">

        <h4 className="font-semibold text-gray-900 mb-3 text-lg">
          Patient Query
        </h4>

        <p className="text-gray-700 leading-7">
          {context.patient_query}
        </p>

      </div>

      <div>

        <h4 className="font-semibold text-gray-900 mb-3 text-lg">
          Doctor Response
        </h4>

        <p className="text-gray-700 leading-7">
          {context.doctor_response}
        </p>

      </div>
    </div>
  )
}