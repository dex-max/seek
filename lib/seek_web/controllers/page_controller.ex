defmodule SeekWeb.PageController do
  use SeekWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
