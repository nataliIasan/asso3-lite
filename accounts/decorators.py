from functools import wraps
from django.contrib.auth.decorators import login_required as _login_required
from django.shortcuts import redirect

# Rende disponibile il decoratore standard di Django sotto un nome coerente
login_required = _login_required


def role_required(expected_role):
    """
    Decoratore personalizzato per limitare l'accesso alle viste in base al ruolo dell'utente.
    
    - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    - Se il ruolo dell'utente (es. 'SCUOLA' o 'ENTE') non corrisponde a quello atteso (expected_role),
      viene reindirizzato alla landing page principale per motivi di sicurezza.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica se l'utente ha effettuato l'accesso
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Verifica se il ruolo dell'utente corrisponde a quello richiesto
            if getattr(request.user, 'role', None) != expected_role:
                return redirect('landing')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
