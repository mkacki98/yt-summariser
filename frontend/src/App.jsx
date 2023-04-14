import { useState } from 'react'
import './App.css'

function App() {
  const [inputValue, setInputValue] = useState("");

  const [submittedURL, setSubmittedURL] = useState("");
  const [submittedTitle, setSubmittedTitle] = useState("");
  const [submittedSummary, setSubmittedSummary] = useState("");
  const [submittedComment, setSubmittedComment] = useState("");

  const [submittedSum, setSubmittedSum] = useState(false);
  const [submittedCom, setSubmittedCom] = useState(false);

  function handleInputChange(event) {
    setInputValue(event.target.value);
  }

  function handleURLSubmit(event) {
    event.preventDefault();
    // run the request
    const inputData = { url: inputValue };

    fetch("http://localhost:8000/videos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(inputData)
    })
    .then(response => {
      if (response.ok) {
        console.log(response)
        return response.json()
      } else {
        throw new Error("Something went wrong.");
      }
    })
    .then(data => {
      console.log(data);

      setSubmittedURL(data.url);
      setSubmittedTitle(data.title);
      setSubmittedSummary(data.summary);

      setSubmittedSum(true)
      setSubmittedCom(false)
    })
    .catch(error => {
      console.error(error);
    });
  }
  
  function handlePostSummary(event) {
    event.preventDefault();
    // run the request
    const inputData = { url: submittedURL };
    console.log(submittedURL)

    fetch("http://localhost:8000/comments", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(inputData)
    })
    .then(response => {
      if (response.ok) {
        console.log(response)
        return response.json()
      } else {
        throw new Error("Something went wrong.");
      }
    })
    .then(data => {
      console.log(data);

      setSubmittedURL(submittedURL);
      setSubmittedTitle(submittedTitle);
      setSubmittedComment(data);

      setSubmittedSum(false)
      setSubmittedCom(true)

    })
    .catch(error => {
      console.error(error);
    });
  }
  
  function handleRandomSubmit(event) {
    event.preventDefault();
    // run the request
    const inputData = { url: inputValue };

    fetch("http://localhost:8000/summary_random", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }})
    .then(response => {
      if (response.ok) {
        console.log(response)
        return response.json()
      } else {
        throw new Error("Something went wrong.");
      }
    })
    .then(data => {
      console.log(data);

      setSubmittedURL(data.url);
      setSubmittedTitle(data.title);
      setSubmittedSummary(data.summary);

      setSubmittedCom(false)
      setSubmittedSum(true)

    })
    .catch(error => {
      console.error(error);
    });
  }
  

  return (
    <div className="grid-container">
      <div className="grid-item">
        <form onSubmit={handleRandomSubmit}>
          <button type="submit"> Display a random summary </button>
        </form>
      </div>
      <div className="grid-item">
        <form onSubmit={handleURLSubmit}>
          <label>
            <button type="submit">Generate summary given URL</button>
            <span>Enter video URL</span>
            <input type="text" value={inputValue} onChange={handleInputChange} />
          </label>
        </form>
      </div>
      <div className="grid-item">
        <form onSubmit={handlePostSummary}>
          <button type="submit">Post current summary</button>
        </form>
      </div>
      <div className="video-info">
      <hr />
      {(submittedSum || submittedCom) && <p><strong>Video URL:</strong> {submittedURL}</p>}
      {(submittedSum || submittedCom) && <p><strong>Title:</strong> {submittedTitle}</p>}
      {(submittedSum || submittedCom) && (
        <p>
          <strong>{submittedCom ? "This comment has been posted:" : "Summary:"}</strong>{" "}
          <br /> {}
          {submittedCom ? submittedComment : submittedSummary}
          <hr />
          </p>
      )}
      </div>
    </div>
  );
}

export default App
