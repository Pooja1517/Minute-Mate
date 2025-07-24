const fs = require("fs");
const axios = require("axios");
const FormData = require("form-data");

const transcribeAudio = async (filePath) => {
  const form = new FormData();
  form.append("audio", fs.createReadStream(filePath));
  const response = await axios.post(
    "http://127.0.0.1:5001/transcribe",
    form,
    { headers: form.getHeaders() }
  );
  return { transcript: response.data.text };
};

module.exports = { transcribeAudio }; 