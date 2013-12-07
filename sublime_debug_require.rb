begin
  require 'byebug'
rescue LoadError
  puts "Byebug gem is not installed for this ruby version: #{RUBY_VERSION}"
  puts "please run 'gem install debugger' while using your default ruby version"
  exit
end

pid = Process.pid
at_exit {
  if $! and pid == Process.pid
    puts "Last exception: #{$!.inspect}"
    puts "Backtrace: "
    puts "#{$@}"
  end
}

Byebug.wait_connection = true
Byebug.start_server "127.0.0.1"

byebug
