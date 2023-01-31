var nodemailer=require('nodemailer')

var transporter=nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'saurabhtribhuvan49@gmail.com',
        pass: 'jmlabamlicuppuvd'
    }

});

var mailOptions={
    from: 'saurabhtribhuvan49@gmaill.com',
    to: 'navjyotsakhalkar7@gmail.com',
    subject: 'Node Mailer',
    html: 'Hello'
    // attachments: [
    //     {
    //         filename: 'logo.png',
    //         patht: './'
    //     }
    // ]
};

transporter.sendMail(mailOptions,(error,info)=>{
    if(error){
        console.log(error);
    }
    else{
        console.log("Email sent"+info.response)
    }
});