const axios = require('axios');

async function testConnection() {
  console.log('Testing connection to Python Whisper API...');
  
  try {
    // Test health endpoint
    const healthResponse = await axios.get('http://127.0.0.1:5001/health', {
      timeout: 5000
    });
    console.log('✅ Health check successful:', healthResponse.data);
    
    // Test if we can reach the transcribe endpoint (without sending file)
    const transcribeResponse = await axios.post('http://127.0.0.1:5001/transcribe', {}, {
      timeout: 5000
    });
    console.log('✅ Transcribe endpoint reachable');
    
  } catch (error) {
    console.log('❌ Connection failed:', error.message);
    if (error.code === 'ECONNREFUSED') {
      console.log('The Python service is not running or not accessible');
    } else if (error.response) {
      console.log('Service responded with error:', error.response.status, error.response.data);
    }
  }
}

testConnection(); 