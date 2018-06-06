    function gettype(){
        $.ajax({
            type: "GET",
            url: 'http://127.0.0.1:5000/gettypes',
            dataType: 'json',
            data: {},
            success: function(result){
                var radiodiv=""
                for(var i=0;i<result.length;i+=1){
                    radiodiv+="<div class='movechange'><img src='分类.png'><label>"+result[i]+"</label></div><br>"
                }
                document.getElementById('type-content').innerHTML=radiodiv
            }
        });
}
        gettype()
