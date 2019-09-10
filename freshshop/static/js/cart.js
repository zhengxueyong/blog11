$(function () {
    $('.add ').click(function () {
        var $that = $(this)
        console.log('点击成功')
        var goodnums= parseInt($that.next().attr('value'))
        goodnums=goodnums+1
        $that.next().attr('value',goodnums)
        // console.log(goodnums)
        var goodid=$that.attr('data-id')
        request_data={
            'goodnums':goodnums,
            'goodid': goodid
        }
        $.get('/fresh/addgoods/',request_data,function (response) {
               console.log(response)
             if (response.status==1){
                 // console.log(response.newprice)
                 $that.parent().parent().next().html(response.newprice+'元')
                 $('#allsum').text(response.allsum)
             }

        })



    })

      $('.minus').click(function () {
        console.log('点击成功')
          var $that = $(this)
        console.log('点击成功')
        var goodnums= parseInt($that.prev().attr('value'))
        goodnums=goodnums-1
          if (goodnums<=1){
              goodnums=1
          }
        $that.prev().attr('value',goodnums)
        // console.log(goodnums)
        var goodid=$that.attr('data-id')
        request_data={
            'goodnums':goodnums,
            'goodid': goodid
        }
        $.get('/fresh/subgoods/',request_data,function (response) {
               console.log(response)
             if (response.status==1){
                 // console.log(response.newprice)
                 $that.parent().parent().next().html(response.newprice+'元')
                  $('#allsum').text(response.allsum)
             }


        })

    })
    // 购物车删除商品
    $('.col08').click(function () {
        var $that=$(this)
        console.log('点击删除成功')
        goodid=$that.attr('data-id')
        console.log(goodid)
        request_data={
            'goodid':goodid
        }
        $.get('/fresh/delgoods/',request_data,function (response) {
            console.log(response)
            if (response.status==1){
               $that.parent().remove()
                $('#newsum').html(response.newsum)
                $('#newsum1').html(response.newsum)
                 $('#allsum').text(response.allsum)

            }

        })


    })


})