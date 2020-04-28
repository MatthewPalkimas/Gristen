var socket = io.connect('http://' + document.domain + ':' + location.port);
      socket.on( 'connect', function() {
        socket.emit( 'my event', {
          data: 'User Connected'
        } )
          id = document.getElementById('gristen').onclick = function() {
             let song_name = $('input.song_name').value()
             socket.emit('song request', {
                song_name : song_name
             })
          }
          id2 = document.getElementById('chat').onclick = function() {
          let user_name = $( 'input.username' ).value()
          let user_input = $( 'input.message' ).value()
          socket.emit( 'my event', {
            user_name : user_name,
            message : user_input
          } )
          $( 'input.message' ).val( '' ).focus()
        }
      } )
      socket.on( 'my response', function( msg ) {
        console.log( msg )
        if( typeof msg.user_name !== 'undefined' ) {
          $( 'h3' ).remove()
          $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
        }
      })

