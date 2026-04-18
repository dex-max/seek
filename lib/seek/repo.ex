defmodule Seek.Repo do
  use Ecto.Repo,
    otp_app: :seek,
    adapter: Ecto.Adapters.Postgres
end
