import Header from "./components/Header"
import Dashboard from "./components/Dashboard"
import Footer from "./components/Footer"
import "./App.css"

function App() {
  return (
    <>
      <Header />
      <main className="main-content">
        <Dashboard />
      </main>
      <Footer />
    </>
  )
}

export default App
