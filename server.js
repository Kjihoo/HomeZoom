const express = require('express');
const app = express();
const {MongoClient, ObjectId } = require('mongodb');

//express틀가져오기

app.use(express.static(__dirname + '/public'))
app.set('view engine', 'ejs')
app.use(express.json())
app.use(express.urlencoded({extended:true}))


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



app.get('/write', async function(req,res){
  res.render('write.ejs')
  
 
});



app.post('/add', async function(req,res){
  console.log(req.body)

  try{

    if (req.body.title == '') {
      res.send('제목을입력해')
  
    }
  
  
    await db.collection('post').insertOne({ title : req.body.title, content : req.body.connect})
  
  } catch(e) {
    console.log(e)
    res.status(500).send('서버에러남')
  }

  
  res.redirect('/list')

});





app.get('/list', async (req,res) =>{
  let result = await db.collection('post').find().toArray()
  //res.send(result[0].title)

  res.render('list.ejs', { 글목록 : result})

  /*  db 내부 테스트
  let result = await db.collection('post').find().toArray()
    console.log(result[0].title)
    res.send(result[0].title)
    */
});



app.get('/time', function(req,res) {
  res.render('time.ejs',{ data : new Date()})

})

app.get('/detail/:id', async (요청, 응답) => {
  try {
    let result = await db.collection('post').findOne({ _id : new ObjectId(요청.params.id) })
    if (result == null) {
      응답.status(400).send('그런 글 없음')
    } else {
      응답.render('detail.ejs', { result : result })
    }
    
  } catch (e){
    응답.send('이상한거 넣지마라')
  }
  
})