export default function ChatBox({

  query,
  setQuery,
  handleSubmit

}) {

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-sky-100 p-8">

      <div className="mb-8">

        <h2 className="text-4xl font-bold text-gray-900 mb-3 leading-tight">
          Intelligent Healthcare Retrieval System
        </h2>

        <p className="text-gray-500 text-lg leading-8 max-w-3xl">
          AI-powered healthcare assistant.
        </p>

      </div>

      <div className="flex flex-col md:flex-row gap-4">

        <textarea
          rows={4}
          placeholder="Describe your symptoms..."
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          className="flex-1 border border-sky-100 bg-sky-50 rounded-2xl p-5 outline-none resize-none text-gray-700 leading-7"
        />

        <button
          onClick={handleSubmit}
          className="bg-sky-700 hover:bg-sky-800 text-white px-8 py-4 rounded-2xl font-semibold"
        >
          Ask AI
        </button>

      </div>
    </div>
  )
}