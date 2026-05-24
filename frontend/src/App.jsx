import React from "react"

import Sidebar from "./components/Sidebar"
import ChatBox from "./components/ChatBox"
import Loader from "./components/Loader"
import ResponseCard from "./components/ResponseCard"
import ContextCard from "./components/ContextCard"

export default function App() {

  const [query, setQuery] = React.useState("")
  const [response, setResponse] = React.useState("")
  const [loading, setLoading] = React.useState(false)
  const [contexts, setContexts] = React.useState([])

  const handleSubmit = async () => {

    if (!query.trim()) return

    setLoading(true)
    setResponse("")
    setContexts([])

    try {

      const res = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            query: query
          })
        }
      )

      const data = await res.json()

      setResponse(data.ai_response)

      setContexts(
        data.retrieved_contexts || []
      )

    } catch (error) {

      console.error(error)

      setResponse(
        "Error generating healthcare response"
      )

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="min-h-screen bg-gradient-to-br from-sky-50 to-white">

      <div className="max-w-7xl mx-auto px-6 py-10">

        <div className="grid lg:grid-cols-[320px_1fr] gap-8">

          <Sidebar />

          <div className="space-y-8">

            <ChatBox
              query={query}
              setQuery={setQuery}
              handleSubmit={handleSubmit}
            />

            {loading && (
              <Loader />
            )}

            {response && (
              <ResponseCard
                response={response}
              />
            )}

            {contexts.length > 0 && (

              <div className="bg-white rounded-3xl shadow-xl border border-sky-100 p-8">

                <h2 className="text-3xl font-bold text-gray-900 mb-8">
                  Retrieved Medical Contexts
                </h2>

                <div className="space-y-8">

                  {contexts.map((context, index) => (

                    <ContextCard
                      key={index}
                      context={context}
                      index={index}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}