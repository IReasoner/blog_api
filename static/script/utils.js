
export function formatTime(timeString) {
  const date = new Date(timeString)

  const local = date.toLocaleDateString("en-NG", {
    month: "long",
    day: "2-digit",
    year: "numeric"
  })
  return local
}