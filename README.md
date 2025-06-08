# Sleep Score

A machine learning application that predicts sleep quality using a custom regression algorithm. The model was trained offline using numpy on real-world data and integrated into a React frontend application, achieving high accuracy in sleep quality prediction.

## Features

- Custom regression algorithm implemented in numpy
- Trained on real-world sleep data
- Interactive React frontend with integrated model
- High prediction accuracy (MSE ~0.32)
- Client-side sleep quality scoring

## Tech Stack

- **Frontend**: React (with integrated ML model)
- **Machine Learning**: Custom regression implementation in NumPy (training)

## Installation

### Prerequisites

- Node.js and npm

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SleepScore.git
cd SleepScore
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start dev
```

## Usage

The web app is deployed and available on Github pages. Simply head to 

<a>https://msaghiri.github.io/SleepScore</a>

Enter data as instructed and click the "predict" button.

## Model Performance

The custom regression algorithm achieves:
- **Mean Squared Error**: ~0.32
- Some features are omitted from the final version for generalizability, slightly diminishing the final mean squared error.
- Trained offline using NumPy on real-world sleep data
- Model weights are integrated directly into the React application

## Contact

If you have questions about the project or want to discuss the custom regression implementation, feel free to reach out!
