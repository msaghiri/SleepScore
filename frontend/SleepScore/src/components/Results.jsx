function Results({ score }) {
    return (
        <div className="results-div">
            <h1>Your sleep score:</h1>
            {score !== null && <h1>{score}</h1>}
        </div>
    );
}

export default Results;
