class RubyVersion
  attr_accessor :version, :gem_name, :init_block, :debug_block

  def initialize(version, gem_name, debug_block, init_block)
    self.version =version
    self.gem_name = gem_name
    self.init_block = init_block
    self.debug_block = debug_block
  end
end

r193 = RubyVersion.new("1.9.3", "debugger", lambda { debugger  }, lambda {  Debugger.wait_connection = true; Debugger.start_remote "127.0.0.1" })
r200 = RubyVersion.new("2.0.0", "byebug", lambda { byebug  }, lambda {  Byebug.wait_connection = true; Byebug.start_server "127.0.0.1" })

versions = {r193.version => r193, r200.version => r200 }

if current_version = versions[RUBY_VERSION]
  begin
    require current_version.gem_name
    current_version.init_block.call

    pid = Process.pid
    at_exit {
      if $! and pid == Process.pid
        puts "Last exception: #{$!.inspect}"
        puts "Backtrace: "
        puts "#{$@}"
      end
    }

    current_version.debug_block.call
  rescue LoadError
    puts "#{current_version.gem_name.capitalize} gem is not installed for ruby version: #{RUBY_VERSION}"
    puts "please run 'gem install #{current_version.gem_name}' while using your default ruby version"
  rescue Errno::EADDRINUSE
    puts "Another process is using the debugging ports (8989,8990)"
    puts "please make sure this ports are free and than run the debugger"
  end
end
