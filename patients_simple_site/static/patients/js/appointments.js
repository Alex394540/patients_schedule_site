function remove_appointment(date_, time_, csrf) {

	let delete_confirmed = confirm('Вы действительно хотите удалить запись?');
	if (!delete_confirmed) return;

	let http = new XMLHttpRequest();
	let params = 'date=' + date_ + '&time=' + time_;
	http.open('POST', '/remove_appointment/', true);

	// Send the proper header information along with the request
	http.setRequestHeader("X-CSRFToken", csrf);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
        if (http.readyState == 4 && http.status == 200) {
        	// change the content of the cell
        	let element_to_change = document.getElementById(date_ + time_);
	    	element_to_change.textContent = '';
            
            // remove event listener
	    	element_to_change.onclick = function() {
                alert('Если вы передумали и хотите вернуть запись - перезагрузите страницу и запишитесь снова');
	    	};

	    	// say to user that everything is fine
            alert('Удалена запись на '.concat(date_, ' ', time_));

	    // Bad request...
	    } else if (http.readyState == 4 && http.status == 400) {
            alert('Что-то пошло не так');
        }
	}
    http.send(params);
}


function add_appointment(date_, time_, csrf) {
    
    let comment = prompt('Введите ваше ФИО', '');
    while (comment === "") {
    	comment = prompt('Введите ваше ФИО', '');
    }

    if (comment === null) return;

    // send request with datetime and comment to the server...
    let http = new XMLHttpRequest();
    let params = 'date=' + date_ + '&time=' + time_ + '&comment=' + comment;
	http.open('POST', '/add_appointment/', true);

	//Send the proper header information along with the request
	http.setRequestHeader("X-CSRFToken", csrf);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	http.onreadystatechange = function() {
		console.log("Added...");
		console.log("Status:", http.status);
        console.log("Ready state:", http.readyState);
	    if (http.readyState == 4 && http.status == 200) {
	    	// change the content of the cell
	    	let element_to_change = document.getElementById(date_ + time_);
	    	element_to_change.textContent = 'Занято';

	    	// Изменим eventListener
	    	element_to_change.onclick = function() {
	    		remove_appointment(date_, time_, csrf);
	    	};
	        
	        // say to user that everything is fine
            alert('Вы записались на '.concat(date_, ' ', time_));

        // Appointment was created in this session
        } else if (http.readyState == 4 && http.status == 405) {
        	alert("Для вас уже найдена запись на прием. Удалите существующую чтобы создать новую.");

        // Bad request...
	    } else if (http.readyState == 4 && http.status == 400) {
            alert('Что-то пошло не так');
	    }
	}
	http.send(params);
}
