module.exports = {
  apps: [
    {
      name: 'project-assistant',
      script: 'uvicorn main:app',
      args: '--host 0.0.0.0 --port 1003',
      interpreter: 'python3',
      env: {
        'OPENAI_API_KEY': process.env.OPENAI_API_KEY,
      },
    },
  ],
};