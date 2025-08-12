// Netlify function to serve the Streamlit app
exports.handler = async function(event, context) {
  // This is a simple proxy function
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/html"
    },
    body: `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>NexusMap Pro - Network Analyzer</title>
          <style>
            html, body { 
              height: 100%; 
              margin: 0; 
              padding: 0; 
              overflow: hidden;
            }
            iframe {
              width: 100%;
              height: 100%;
              border: none;
            }
            .loading {
              position: fixed;
              top: 0;
              left: 0;
              right: 0;
              bottom: 0;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              background-color: #0E1117;
              color: white;
              font-family: sans-serif;
              z-index: 1000;
            }
            .spinner {
              width: 50px;
              height: 50px;
              border: 5px solid rgba(255, 255, 255, 0.3);
              border-radius: 50%;
              border-top-color: #1f77b4;
              animation: spin 1s ease-in-out infinite;
              margin-bottom: 20px;
            }
            @keyframes spin {
              to { transform: rotate(360deg); }
            }
          </style>
        </head>
        <body>
          <div class="loading" id="loading">
            <div class="spinner"></div>
            <h2>Loading NexusMap Pro...</h2>
            <p>Please wait while we prepare your network visualization.</p>
          </div>
          
          <iframe src="https://nexusmap-pro.streamlit.app" id="streamlitApp" onload="hideLoading()"></iframe>
          
          <script>
            function hideLoading() {
              document.getElementById('loading').style.display = 'none';
            }
            
            // If loading takes too long, hide it anyway after 10 seconds
            setTimeout(hideLoading, 10000);
          </script>
        </body>
      </html>
    `
  };
};
