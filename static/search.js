document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#form_js').onsubmit = () => {
        alert("Searching please wait!")
        var request = new XMLHttpRequest();
        var myInput = document.querySelector('#myInput').value;
        request.open("POST", "/api/search");
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify({ "search": myInput}));
        request.onload = () => {
            var data = JSON.parse(request.responseText);
            if (data) {
                var contents = "";
                let json_data = data["bookdata"];
                for (x in json_data) {
                    contents += '<a class="item" id="#book_details" href="#" ' + 'onclick=generate_book_details("'+json_data[x]["isbn"]+'")' + '> <div class="content" style="border: 1px solid black"> <div class="header"><b>'+ json_data[x]["title"]+'</b></div></div></a>'
                }
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }
        const data = new FormData();
        data.append('myInput', myInput);
        return false;
    };
});

function generate_book_details(isbn) {
    alert("Fetching Data   please wait!")
    var request = new XMLHttpRequest();
    request.open('GET', '/api/book?isbn='+isbn);
    request.onload = function() {
        if (request.status === 200) {
            let data=JSON.parse(request.responseText);
            if ((data[0]['user_rating'] != "0") && (data[0]['user_review'] != "0")) {
                const content = '<div class="content" style="border: 1px solid black">'+
                '<div class = "name"><h1>'+data[0]["name"]+"'s Display Board"+'</h1></div><hr class="new4">'+
                '<div class = "Book"><div class="flex-container"><section class="container" style="display: flex;">'+
                '<div class="left-half"><article><center><img src ="'+data[0]["img"]+'" alt = "Image of a Book"></center></article></div>'+
                '<div class="right-half"><article><div class = "details"><br><br><br>'+
                '<center><p>Book Name : "'+data[0]["title"]+'"</p><p>Author : "'+data[0]["author"]+'"</p><p>ISBN : "'+data[0]["isbn"]+'"</p><p>Year of Publication : "'+data[0]["year"]+'"</p><p>Average Rating : "'+data[0]["rating"]+'"</p><p>Number of reviewers : "'+data[0]["review"]+'"</p></center>'+
                '</div></article></div></section></div><hr class="new3"><center><div class = "button"><h3>Your Review</h3><br>'+
                '<form method="POST" class="form-border" id=form_review><div class="flex-container"><section class="container" style="display: flex;">'+
                '<div class="left-half"><article><br><br><br><br><br><div class = "select3"><label for="rating" style = "font-weight: bold; color: black;">Rate this book</label>'+
                '<select id="rating" name="rating" class="form-control" required><option value="1">1</option><option value="2">2</option>'+
                '<option selected value="3">3</option><option value="4">4</option><option value="5">5</option></select></div></article></div>'+
                '<div class="right-half"><article><div class="rating-input"><br>'+
                '<textarea name="matter" style= "color: black;" id="review" class="form-control" rows="10" placeholder="Write your review here" required></textarea>'+
                '</div></article></div></section></div><div><button class="rating-btn" type="submit" onclick=generate_review("'+data[0]["isbn"]+'")>'+"Edit"+'</button></div></form></div></center></div>'+
                '<hr class="new3"><div class = "review" style = "display: flex; justify-content: center; color: black; float: top; font-style: normal; font-weight: bolder; font-size: x-small;">'+
                '<ul><center><li style = "font-size: 20px; font-style: normal;">Your Previous Rating & Review</li><hr class="new3">'+
                '<li style = "font-size: 20px; font-style: normal;">'+data[0]["user_rating"]+'/5</li><br><li style = "color: black; font-size: 20px;">"'+data[0]["user_review"]+'"</li></center>'+
                '</ul></div></div></div>'
                document.querySelector('#book_details').innerHTML = content;
            }   
            else {
                const content = '<div class="content" style="border: 1px solid black">'+
                '<div class = "name"><h1>'+data[0]["name"]+"'s Display Board"+'</h1></div><hr class="new4">'+
                '<div class = "Book"><div class="flex-container"><section class="container" style="display: flex;">'+
                '<div class="left-half"><article><center><img src ="'+data[0]["img"]+'" alt = "Image of a Book"></center></article></div>'+
                '<div class="right-half"><article><div class = "details"><br><br><br>'+
                '<center><p>Book Name : "'+data[0]["title"]+'"</p><p>Author : "'+data[0]["author"]+'"</p><p>ISBN : "'+data[0]["isbn"]+'"</p><p>Year of Publication : "'+data[0]["year"]+'"</p><p>Average Rating : "'+data[0]["rating"]+'"</p><p>Number of reviewers : "'+data[0]["review"]+'"</p></center>'+
                '</div></article></div></section></div><hr class="new3"><center><div class = "button"><h3>Your Review</h3><br>'+
                '<form method="POST" class="form-border" id=form_review><div class="flex-container"><section class="container" style="display: flex;">'+
                '<div class="left-half"><article><br><br><br><br><br><div class = "select3"><label for="rating" style = "font-weight: bold; color: black;">Rate this book</label>'+
                '<select id="rating" name="rating" class="form-control" required><option value="1">1</option><option value="2">2</option>'+
                '<option selected value="3">3</option><option value="4">4</option><option value="5">5</option></select></div></article></div>'+
                '<div class="right-half"><article><div class="rating-input"><br>'+
                '<textarea name="matter" style= "color: black;" id="review" class="form-control" rows="10" placeholder="Write your review here" required></textarea>'+
                '</div></article></div></section></div><div><button class="rating-btn" type="submit" onclick=generate_review("'+data[0]["isbn"]+'")>'+"Submit"+'</button></div></form></div></center></div>'+
                '</div></div>'
                document.querySelector('#book_details').innerHTML = content;
            }
        }
        else {
            document.querySelector('#book_details').innerHTML = "Error";
        }
    };
    request.send();
}

function generate_review(isbn) {
    alert("Updating Data-base")
    document.querySelector('#form_review').onsubmit = () => {
        var rate = document.querySelector('#rating').value;
        var review = document.querySelector('#review').value;
        var req = new XMLHttpRequest();
        req.open("POST", "/api/submit_review");
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        req.send(JSON.stringify({ "rating": rate, "review": review, "isbn": isbn}));
        req.onload = () => {
            var data = JSON.parse(req.responseText);
            generate_book_details(isbn)            
        }
        return false
    }
}
