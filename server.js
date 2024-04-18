const express = require('express');
const app = express();
//express틀가져오기

app.use(express.static(__dirname + '/public'))

const { MongoClient } = require('mongodb')

let db
const url = 'mongodb+srv://dmlqk123:2019@jihoo123.vgv0trk.mongodb.net/?retryWrites=true&w=majority&appName=jihoo123'
new MongoClient(url).connect().then((client)=>{
  console.log('DB연결성공')
  db = client.db('forum') //db이름

  app.listen(8080, function(){
    console.log('listening on 8080')

});
}).catch((err)=>{
  console.log(err)
})




app.get('/', function(req,res){
    res.sendFile(__dirname + '/index.html')

});


app.get('/reg', function(req,res){
    res.send('회원가입창')

});

app.get('/news', function(req,res){
    db.collection('post').insertOne({title : '테스트'})

});


