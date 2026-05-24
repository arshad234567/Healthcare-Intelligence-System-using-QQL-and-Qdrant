const BASE_URL = "https://healthcare-intelligence-system-using-qql.onrender.com"
export async function askHealthcareAI(query) {

  const response = await fetch(

    `${BASE_URL}/ask`,

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

  if (!response.ok) {

    throw new Error(
      "Failed to fetch healthcare response"
    )
  }

  return await response.json()
}