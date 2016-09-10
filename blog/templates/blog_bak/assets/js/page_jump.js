/**
 * Created by sdy on 9/22/15.
 */

function page_jump(type, current_page, last_page,url) {
    var search_name = $('#search_name').val();
    var search_type = $('#search_type').val();
    if (search_type)
    {
        if (type == 'fist') {
            if (current_page != 1) {
                window.location.href = url+"?pageNum=1" + "&search_name=" + search_name +"&search_type="+search_type
            }
        }
        if (type == 'pre') {
            if (current_page != 1) {
                window.location.href = url+"?flag=" + type + "&pageNum=" + current_page + "&search_name=" + search_name+"&search_type="+search_type
            }
        }
        if (type == 'num') {
            window.location.href = url+"?pageNum=" + current_page + "&search_name=" + search_name+"&search_type="+search_type
        }
        if (type == "next") {
            if (current_page != last_page) {
                window.location.href = url+"?flag=" + type + "&pageNum=" + current_page + "&search_name=" + search_name+"&search_type="+search_type
            }
        }
        if (type == "last") {
            if (current_page != last_page) {
                window.location.href = url+"?pageNum=" + last_page + "&search_name=" + search_name+"&search_type="+search_type
            }
        }
    }
    else{
        if (type == 'fist') {
            if (current_page != 1) {
                window.location.href = url+"?pageNum=1" + "&search_name=" + search_name
            }
        }
        if (type == 'pre') {
            if (current_page != 1) {
                window.location.href = url+"?flag=" + type + "&pageNum=" + current_page + "&search_name=" + search_name
            }
        }
        if (type == 'num') {
            window.location.href = url+"?pageNum=" + current_page + "&search_name=" + search_name
        }
        if (type == "next") {
            if (current_page != last_page) {
                window.location.href = url+"?flag=" + type + "&pageNum=" + current_page + "&search_name=" + search_name
            }
        }
        if (type == "last") {
            if (current_page != last_page) {
                window.location.href = url+"?pageNum=" + last_page + "&search_name=" + search_name
            }
        }
    }

}