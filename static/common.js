$(document).ready(function () {


   /* $.get("http://10.32.58.130:5000/manager/M1",{},function (data) {
        console.log("get call")
        console.log(data)
    });*/


    $.get("/user", {}, function (ManagerName) {

        $.get("http://localhost:5000/manager/"+ManagerName,{},function (Projects) {
            $("#dynamic_div").remove();
            var dynamicdiv = $("<div id=\"dynamic_div\">");

            $.each(Projects, function(ProjectName, ProjectStruct){
                var P1 = $("<h1>");
                P1.text(ProjectName);
                dynamicdiv.append(P1);
                var form=$("<form>");

                // if ProjectStruct.fixed is true add a class to the student and dont add select button
                for (var i = 0; i < ProjectStruct.students.length; i++) {
                var input=$("<input>");
                input.attr("type","radio");
                    input.attr("name",ProjectName);
                    input.attr("value",ProjectStruct.students[i]);
                    form.append(input)
                var student = $("<a>");
                    student.attr("href", "/static/"+ProjectStruct.students[i]+".pdf")
                    student.attr("target","=\"_blank\"")
                    student.text(ProjectStruct.students[i])
                    form.append(student);
                    form.append("<br>");

                }
                var button=$("<button>");
                dynamicdiv.append(form)
                button.attr("id",ProjectName);
                button.addClass("submit")
                button.text("Submit")
                dynamicdiv.append(button)

            });

            $("#Projects").append(dynamicdiv);
        });
    });


   $(document).on("click",".submit",function () {
       var project=this.id;
       var jsondata = '{'
       jsondata += "\"student_name\":" +"\""+$("input[name="+project+"]:checked").val()+"\"" + "}";
       console.log(jsondata)

       $.ajax({
           url: 'http://localhost:5000/project/'+project,
           type: 'POST',
           data: jsondata,
           success: function (result) {
               alert("submitted Successfully");
           },
           error: function (xhr, status, error) {
               alert("Network Conncection Problem!")
           }
       })
    });




});