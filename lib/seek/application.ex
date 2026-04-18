defmodule Seek.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      SeekWeb.Telemetry,
      Seek.Repo,
      {DNSCluster, query: Application.get_env(:seek, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: Seek.PubSub},
      # Start a worker by calling: Seek.Worker.start_link(arg)
      # {Seek.Worker, arg},
      # Start to serve requests, typically the last entry
      SeekWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Seek.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    SeekWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
