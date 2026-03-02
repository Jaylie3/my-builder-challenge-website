const AWS = require('aws-sdk');
const ses = new AWS.SES({ region: process.env.AWS_REGION || 'us-east-1' });

exports.handler = async (event) => {
  try {
    // Parse the form data from the request body
    const body = JSON.parse(event.body);
    const { name, email, message } = body;

    // Validate input
    if (!name || !email || !message) {
      return {
        statusCode: 400,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ error: 'All fields are required' })
      };
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return {
        statusCode: 400,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ error: 'Invalid email address' })
      };
    }

    // Send email via SES
    const params = {
      Source: process.env.SES_FROM_EMAIL || 'noreply@yourdomain.com',
      Destination: {
        ToAddresses: [process.env.SES_TO_EMAIL || 'your-email@example.com']
      },
      Message: {
        Subject: {
          Data: `New Contact Form Submission from ${name}`
        },
        Body: {
          Text: {
            Data: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
          },
          Html: {
            Data: `
              <h2>New Contact Form Submission</h2>
              <p><strong>Name:</strong> ${name}</p>
              <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
              <h3>Message:</h3>
              <p>${message.replace(/\n/g, '<br>')}</p>
            `
          }
        }
      }
    };

    await ses.sendEmail(params).promise();

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        success: true, 
        message: 'Thank you for your message! We\'ll get back to you soon.' 
      })
    };

  } catch (error) {
    console.error('Error sending email:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        error: 'Failed to send message. Please try again later.' 
      })
    };
  }
};
