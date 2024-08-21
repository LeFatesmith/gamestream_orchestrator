# GameStream Orchestrator Bot Setup

## Status: WIP

## Requirements
- Python 3.8 or higher
- Pipenv

## Setup Instructions

1. Clone the repository:
    ```
    git clone https://github.com/LeFatesmith/gamestream_orchestrator.git
    cd gamestream_orchestrator
    ```

2. Install the dependencies:
    ```
    pip install pipenv
    pipenv install
    ```

3. Run the bot:
    ```
    pipenv run python scripts/run_bot.py
    ```

4. Customize the configurations in `configs/bot_config.yaml` as needed.

## Features

- Game Management
- Twitch Integration
- OBS Control
- Mod Management

## Tasks

### 1. Code Integration
- **Merge `TwitchVotingBot`**: Integrate `TwitchVotingBot` with the existing `TwitchBot` and `GameManager` classes.
- **Refactor `run_bot.py`**: Decide on running both bots sequentially or in parallel.
- **Functional Testing**: Finalize and validate the `TwitchVotingBot` functional test for compatibility.

### 2. Configuration Management
- **Sensitive Data Handling**: Secure API keys, Steam IDs, and other sensitive data in `config.yaml`.
- **Centralize Configs**: Ensure all configurations are managed through `config.yaml`.

### 3. User Experience Improvements
- **Voting UI**: Enhance pie chart visualization and spinner for a better user experience.
- **Error Handling**: Strengthen error handling, especially for game launching and macro execution.

### 4. Documentation
- **Detailed Instructions**: Update README with comprehensive setup and usage instructions.
- **Contributors Guide**: Add guidelines for contributions, including coding standards and testing procedures.

### 5. Future Features
- **Expand Game Options**: Add more games and macros to the voting system.
- **Multi-User Voting**: Support voting across different channels or streams.
- **OBS Integration**: Investigate integration with OBS for automated scene changes based on game selection.

### 6. Testing
- **Unit Tests**: Develop and expand unit tests for new features.
- **CI/CD Pipeline**: Implement automated testing using GitHub Actions or another CI/CD tool.

## License
MIT License
