document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form_js').onsubmit = () => {
    // document.querySelector(".search-btn").onclick = () => {
        alert("Searching")
        // Initialize new request
        var request = new XMLHttpRequest();
        var myInput = document.querySelector('#myInput').value;
        console.log(myInput)
        // print(myInput)
        request.open("POST", "/api/search");
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify({ "search": myInput}));
        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            var data = JSON.parse(request.responseText);
            // console.log("--------------------",data)
            // Update the result div
            if (data) {
                // console.log("Hi")
                var contents = "";
                let json_data = data["bookdata"];
                for (x in json_data) {
                    // contents += '<tr> <th scope="row"> <a id="#book_details" href="#" onclick=get_book_details("'+ json_data[x]["isbn"] + '")>' + json_data[x]["title"] +'</a> </th> </tr>';
                    contents += '<a class="item" id="#book_details" href="#" onclick=generate_book_details("'+ json_data[x]["isbn"] + '")> <div class="content" style="border: 1px solid black"> <div class="header"><b>'+ json_data[x]["title"] +'</b></div></div></a>'
                    // contents = "<a class="item" href="{{ url_for('bookInfo', isbn = book.isbn) }}">
                    //                 <div class="content" style="border: 1px solid black">
                    //                     <div class="header"><b>{{ book.title }}</b></div>
                    //                     <br>
                    //                     <div class="extra">
                    //                     </div>
                    //                     <div class="description">
                    //                     <p> <b>The Author: </b>{{ book.author }}</p>
                    //                     <p> <b>The ISBN number of the book: </b> {{ book.isbn }}</h2>
                    //                     <p class="right floated"> <b><b>Published in:</b> </b>{{ book.year }}</p>
                    //                     </div>
                                
                    //                 </div>
                    //             </a>"
                }
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                console.log('bye');
                print('bye')
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('myInput', myInput);

        // // Send request
        // request.send(data);
        return false;
    };

});