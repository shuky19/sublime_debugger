if RUBY_VERSION == "1.9.3"
  begin
    require 'debugger'
  rescue LoadError
    puts "Debugger gem is not installed for this ruby version: #{RUBY_VERSION}"
    puts "please run 'gem install debugger' while using your default ruby version"
    exit
  end
elsif RUBY_VERSION == "2.0.0"
  begin
    require 'byebug'
  rescue LoadError
    puts "Byebug gem is not installed for this ruby version: #{RUBY_VERSION}"
    puts "please run 'gem install byebug' while using your default ruby version"
    exit
  end
end



begin
  Byebug.wait_connection = true
  Byebug.start_server "127.0.0.1"
rescue Errno::EADDRINUSE
  puts "Another process is using the debugging ports (8989,8990)"
  puts "please make sure this ports are free and than run the debugger"
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

byebug
